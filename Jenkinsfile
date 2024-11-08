pipeline {
    agent any

    environment {
        ACCURACY_THRESHOLD = "0.80"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/rbcse/ci-cd'

            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    docker.compose.build()
                }
            }
        }

        stage('Run Microservices') {
            steps {
                script {
                    docker.compose.up()
                }
            }
        }

        stage('Train Model') {
            steps {
                script {
                    def inputResponse = sh(script: 'curl -X POST http://localhost:5000/input -d \'{"dataset": "iris", "n_estimators": 100, "max_depth": 3}\' -H "Content-Type: application/json"', returnStdout: true).trim()
                    echo "Input response: ${inputResponse}"
                }
            }
        }

        stage('Check Accuracy') {
            steps {
                script {
                    def outputResponse = sh(script: 'curl http://localhost:5002/output', returnStdout: true).trim()
                    echo "Output response: ${outputResponse}"
                    def accuracy = sh(script: 'echo $outputResponse | jq -r .accuracy', returnStdout: true).trim()
                    if (accuracy.toDouble() < env.ACCURACY_THRESHOLD.toDouble()) {
                        error("Model accuracy is below the threshold, retrying with different hyperparameters...")
                    }
                }
            }
        }

        stage('Retrain Model with Different Hyperparameters') {
            when {
                expression { currentBuild.result == 'FAILURE' }
            }
            steps {
                script {
                    def inputResponse = sh(script: 'curl -X POST http://localhost:5000/input -d \'{"dataset": "iris", "n_estimators": 200, "max_depth": 5}\' -H "Content-Type: application/json"', returnStdout: true).trim()
                    echo "Retrying with different hyperparameters: ${inputResponse}"
                }
            }
        }
    }

    post {
        success {
            echo "Model training and deployment successful!"
        }
        failure {
            echo "Model training failed, retrying..."
            build job: 'ml-training-job', parameters: []
        }
    }
}
