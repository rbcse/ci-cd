from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/output', methods=['POST'])
def get_output():
    data = request.json
    status = data['status']
    accuracy = data['accuracy']
    #bct

    if status == 'success':
        return jsonify({'message': 'Model saved with accuracy', 'accuracy': accuracy})
    else:
        return jsonify({'message': 'Model accuracy not sufficient', 'accuracy': accuracy})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
