# model.py

import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from data import reponses,questions, labels,ops
from handle_functions import *
import re
import random
import pickle
import logging
from pathlib import Path

import ssl
import os




try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Set NLTK data path for deployment
nltk_data_dir = os.path.join(os.getcwd(), 'nltk_data')
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir)
nltk.data.path.append(nltk_data_dir)

# Download required NLTK data with error handling
print("Downloading NLTK data...")
datasets = ['punkt', 'punkt_tab', 'stopwords', 'wordnet', 'omw-1.4']

for dataset in datasets:
    try:
        nltk.data.find(f'tokenizers/{dataset}')
        print(f"{dataset} already downloaded")
    except LookupError:
        try:
            nltk.data.find(f'corpora/{dataset}')
            print(f"{dataset} already downloaded")
        except LookupError:
            print(f"Downloading {dataset}...")
            nltk.download(dataset, download_dir=nltk_data_dir)
            print(f"{dataset} downloaded successfully!")

print("All NLTK data ready!")







# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
MODEL_VERSION = os.getenv('MODEL_VERSION', '1.0.0')
MODEL_PATH = os.getenv('MODEL_PATH', 'models/chatbot_model.pkl')

# Initialize
stop_words = set(stopwords.words("french")) | set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()





def preprocess(text):
    try:
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        words = text.split()
        words = [w for w in words if w not in stop_words]
        words = [lemmatizer.lemmatize(w) for w in words]
        return " ".join(words)
    except Exception as e:
        logger.error(f"Error in preprocess: {e}")
        return text.lower()



# -----------------------
# Text preprocessing
# -----------------------
def nettoyer(text):

    try:
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        tokens = word_tokenize(text)
        return " ".join(tokens)
    except Exception as e:
        logger.error(f"Error in nettoyer: {e}")
        return text.lower()

questions_nettoyees = [nettoyer(q) for q in questions]


def split_questions(text):
    # Split by common delimiters: '.', '?', '!', 'et', ','
    sentences = re.split(r'[?.!]| et |,', text)
    # Remove empty strings and strip whitespace
    return [s.strip() for s in sentences if s.strip()]



# -----------------------
# Functionalities
# -----------------------
import operator

def calc(expr):
    try:
        # Remove spaces
        expr = expr.replace(" ", "")

        # Match a simple pattern: number operator number
        match = re.match(r'(-?\d+\.?\d*)([\+\-\*/])(-?\d+\.?\d*)$', expr)
        if match:
            a, op, b = match.groups()
            a = float(a)
            b = float(b)
            if op == '/' and b == 0:
                return "Erreur : division par zéro."
            result = ops[op](a, b)
            return f"Le résultat est : {result}"
    except Exception as e:
        logger.error(f"Error in calc: {e}")
    return None


# -----------------------
# Train ML model
# -----------------------

def train_model(intents):
   
    logger.info("Training model...")

    try:
        # Prepare training data
        X = [preprocess(x) for x in questions]

        # Create and train vectorizer
        vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(1, 2),
            max_df=0.9
        )

        X_vec = vectorizer.fit_transform(X)

        # Train model
        model = LogisticRegression(max_iter=1000)
        model.fit(X_vec, labels)

        logger.info("Model trained successfully")
        return vectorizer, model

    except Exception as e:
        logger.error(f"Error training model: {e}")
        raise



def save_model(vectorizer, model, path=MODEL_PATH):
    
    try:
        # Create directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)

        # Save model
        with open(path, 'wb') as f:
            pickle.dump({
                'vectorizer': vectorizer,
                'model': model,
                'version': MODEL_VERSION
            }, f)

        logger.info(f"Model saved to {path}")

    except Exception as e:
        logger.error(f"Error saving model: {e}")
        raise


def load_model(path=MODEL_PATH):
    
    try:
        if not path.exists():
            logger.warning(f"Model file not found at {path}")
            return None

        with open(path, 'rb') as f:
            data = pickle.load(f)

        logger.info(f"Model loaded from {path} (version: {data.get('version', 'unknown')})")
        return data['vectorizer'], data['model']

    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None


def get_or_train_model(intents):
    
    # Try to load existing model
    result = load_model()

    if result:
        return result

    # Model doesn't exist, train new one
    logger.info("No saved model found, training new model...")
    vectorizer, model = train_model(intents)

    # Save for next time
    save_model(vectorizer, model)

    return vectorizer, model


# Initialize model (load or train)
try:
    vectorizer, model = get_or_train_model({'intents': []})  # Pass your actual intents here
except Exception as e:
    logger.error(f"Failed to initialize model: {e}")
    vectorizer, model = None, None



# -----------------------
# Chatbot response function
# -----------------------

def rule_based_intent(message):

    try:
        msg = normalize_text(message)

        if any(expr in msg for expr in ["hello", "hi", "hey", "bonjour", "salut"]):
            return "salutation"

        if any(expr in msg for expr in ["how are you", "comment ça va", "ça va", "what's up", "comment ca va","ca va","how are you","how are you doing","whats up"]):
            return "etat"

        if any(expr in msg for expr in ["who are you", "qui es-tu", "que fais-tu", "what do you do"]):
            return "identite"

        if any(word in msg for word in ["horaire", "horaires", "heure", "ouvrir", "fermer","opening hours", "working hours"]):
            return "horaire"

        if any(word in msg for word in ["contact", "email", "téléphone", "numero","phone"]):
            return "contact"

    except Exception as e:
        logger.error(f"Error in rule_based_intent: {e}")

    return None



def chatbot_with_fallback(message,session,threshold=0.3):

    forced_intent = rule_based_intent(message)
    try:

        if forced_intent:
            response = reponses.get(forced_intent, reponses.get("unknown", "Je ne comprends pas."))
            if isinstance(response, list):
                return random.choice(response)
            return response,forced_intent

        # Check if model is available
        if vectorizer is None or model is None:
            return "Le modèle n'est pas disponible. Veuillez réessayer plus tard.", None


        message_clean = nettoyer(message)
        vect = vectorizer.transform([message_clean])

        proba = model.predict_proba(vect)[0]
        max_prob = max(proba)
        intention = model.classes_[proba.argmax()]

        if max_prob < threshold:

            # Use context if available
            last_intent = session.get("last_intent")
            if last_intent:
                intention = last_intent
                logger.info(f"Low confidence ({max_prob:.2f}), using context: {intention}")
            else:
                return reponses.get("unknown", "Je ne suis pas sûr de comprendre. Pouvez-vous reformuler ?"), None

        response = reponses.get(intention, reponses.get("unknown", "Je ne comprends pas."))

        if isinstance(response, list):
            response=random.choice(response)

        return response,intention

    except Exception as e:
        logger.error(f"Error in chatbot_with_fallback: {e}")
        return "Désolé, une erreur s'est produite. Veuillez réessayer.", None



def chatbot_enhanced(message,session,threshold=0.3):
    print("ENTER chatbot_enhanced")
    try:
        # Input validation
        if not message or not message.strip():
            return "Veuillez entrer un message.", None, None

        if len(message) > 1000:
            return "Votre message est trop long (maximum 1000 caractères).", None, None

        responses = []
        detected_intent = None
        email_extracted = None

        # Check for email extraction
        email_response, email_extracted = handle_email(message)
        if email_response:
            return email_response, "email_extraction", email_extracted

        # Check for email recall
        recall = handle_email_recall(message, session)
        if recall:
            return recall, "email_recall", None


        # Split into multiple questions
        questions = re.split(r'[?.!]| et |,', message)
        questions = [q.strip() for q in questions if q.strip()]

        intents=[]

        for q in questions:
            # Try special handlers first
            date_time_response = handle_datetime(q)
            if date_time_response:
                responses.append(date_time_response)
                intents.append("datetime")
                continue

            bye_response = handle_goodbye(q)
            if bye_response:
                responses.append(bye_response)
                intents.append("goodbye")
                continue

            calcul = calc(q)
            if calcul:
                responses.append(calcul)
                intents.append("calculator")
                continue

            # Fallback to ML model
            response, intent = chatbot_with_fallback(q, session, threshold)
            responses.append(response)
            if intent:
                intents.append(intent)

            # Use the last detected intent as the main intent
            detected_intent = intents[-1] if intents else None
        print("EXIT chatbot_enhanced")
        return " ".join(responses), detected_intent, email_extracted

    except Exception as e:
        logger.error(f"Error in chatbot_enhanced: {e}")
        return "Désolé, une erreur s'est produite. Veuillez réessayer.", None, None


# Script to train and save model manually
if __name__ == "__main__":
    print("Training model...")
    from data import questions, labels

    # Train model
    vec, mod = train_model({'intents': []})

    # Save model
    save_model(vec, mod)

    print(f"Model trained and saved to {MODEL_PATH}")


