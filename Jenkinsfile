pipeline {
    agent any

    environment {
        ACCURACY_THRESHOLD = "0.80"
        RETRY_COUNT = 0
        MAX_RETRIES = 3
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
                    def accuracy = outputResponse.tokenize(',').find { it.contains('accuracy') }?.split(':')[1]?.trim()?.toDouble()
                    echo "Model accuracy: ${accuracy}"
                    
                    if (accuracy == null || accuracy < env.ACCURACY_THRESHOLD.toDouble()) {
                        env.RETRY_COUNT = env.RETRY_COUNT.toInteger() + 1
                        if (env.RETRY_COUNT.toInteger() <= env.MAX_RETRIES.toInteger()) {
                            error("Model accuracy is below the threshold, retrying with different hyperparameters...")
                        } else {
                            error("Exceeded max retries. Model accuracy did not meet the threshold.")
                        }
                    }
                }
            }
        }

        stage('Retrain Model with Different Hyperparameters') {
            when {
                expression { currentBuild.result == 'FAILURE' && env.RETRY_COUNT.toInteger() <= env.MAX_RETRIES.toInteger() }
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
            echo "Model training failed, exceeded retries or another issue occurred."
        }
    }
}
