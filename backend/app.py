# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from model import chatbot_enhanced

import ssl

# Fix SSL certificate issues for NLTK downloads
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download required NLTK data
print("Downloading NLTK data...")
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
print("NLTK data downloaded successfully!")

app = Flask(__name__)
CORS(app)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    response = chatbot_enhanced(message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)



