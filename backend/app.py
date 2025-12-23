# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from model import chatbot_enhanced


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    response = chatbot_enhanced(message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)






