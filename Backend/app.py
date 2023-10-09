from flask import Flask

app = Flask(__name__)

@app.route('/api/message', methods=['GET'])
def get_message():
    message = {'message': 'Hello from Python!'}
    return jsonify(message)

if __name__ == '__main__':
    app.run(debug=True)