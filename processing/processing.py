import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_data():
    # Get hyperparameters from the input request
    hyperparams = request.json
    
    # Pre-loaded dataset (already available in the system)
    dataset = load_iris()  # This could be replaced by any dataset already loaded in the backend

    # Get hyperparameters for the model, with default values if not provided
    n_estimators = hyperparams.get('n_estimators', 100)
    max_depth = hyperparams.get('max_depth', None)
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(dataset.data, dataset.target, test_size=0.2)
    
    # Train the model with the received hyperparameters
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    model.fit(X_train, y_train)
    
    # Evaluate the model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    # Save model if accuracy > threshold
    if accuracy > 0.8:
        joblib.dump(model, 'model.pkl')
        return jsonify({'status': 'success', 'accuracy': accuracy})
    else:
        return jsonify({'status': 'failure', 'accuracy': accuracy})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
