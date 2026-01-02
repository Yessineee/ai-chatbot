# Intelligent Chatbot – Internship Assistant

This is a **personal project** showcasing the development of an intelligent, bilingual (French/English) chatbot with context awareness, session management, 
and specialized handlers for common tasks that assists users with internship-related questions through natural language interaction.

The project demonstrates a **hybrid NLP approach**, combining Machine Learning and
rule-based logic, exposed through a REST API and a modern web interface.

---

##  Features

- Intent classification using Machine Learning
- Typo tolerance with character n-grams
- Confidence threshold for unknown inputs
- Context-aware responses remembering conversation history
- Multi-question understanding in a single message
- Date & time detection
- Email extraction and storage
- Hybrid architecture (ML + rules)
- REST API (Flask)
- Web interface (React + TypeScript)

---

## Tech Stack

### Backend
- Python
- Flask
- Scikit-learn
- NLTK

### Frontend
- React
- TypeScript
- Lovable.dev

---

### Backend

-Clone the repository
git clone https://github.com/Yessineee/ai-chatbot.git
cd ai-chatbot/backend

-Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

-Install dependencies
pip install -r requirements.txt

-Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

-Train the model (first time only)
python train_model_script.py

-Run the server
python app.py



### Frontend

cd frontend

-Install dependencies
npm install

-Run development server
npm run dev


###API Documentation

-Base URL:
Local: http://localhost:5000
Production: https://yessine-chatbot.vercel.app


###Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

1-Fork the repository
2-Create your feature branch (git checkout -b feature/AmazingFeature)
3-Commit your changes (git commit -m 'Add some AmazingFeature')
4-Push to the branch (git push origin feature/AmazingFeature)
5-Open a Pull Request


###Contact:
For questions or feedback, please open an issue on GitHub or contact me directly.

⭐ If you find this project useful, please consider giving it a star on GitHub!

---

🚧 This project is under active development. Improvements will be added gradually.
