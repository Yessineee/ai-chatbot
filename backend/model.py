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


stop_words = set(stopwords.words("french")) | set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


# ======================
# CONTEXT MEMORY
# ======================
conversation_context = {
    "last_intent": None,
    "email": None
}


def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    words = [lemmatizer.lemmatize(w) for w in words]
    return " ".join(words)

# -----------------------
# Text preprocessing
# -----------------------
def nettoyer(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    tokens = word_tokenize(text)
    return " ".join(tokens)

questions_nettoyees = [nettoyer(q) for q in questions]


def split_questions(text):
    # Split by common delimiters: '.', '?', '!', 'et', ','
    sentences = re.split(r'[?.!]| et |,', text)
    # Remove empty strings and strip whitespace
    return [s.strip() for s in sentences if s.strip()]


import operator



# -----------------------
# Functionalities
# -----------------------


def calc(expr):

    # Remove spaces
    expr = expr.replace(" ", "")

    # Match a simple pattern: number operator number
    match = re.match(r'(-?\d+\.?\d*)([\+\-\*/])(-?\d+\.?\d*)$', expr)
    if match:
        a, op, b = match.groups()
        try:
            a = float(a)
            b = float(b)
            result = ops[op](a, b)
            return f"Le résultat est : {result}"
        except ZeroDivisionError:
            return "Erreur : division par zéro."
    return None  # Not a valid math expression

# -----------------------
# Train ML model
# -----------------------

vectorizer = TfidfVectorizer(analyzer="char_wb",ngram_range=(1, 2),max_df=0.9)
X = [preprocess(x) for x in questions]
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vec, labels)

# -----------------------
# Chatbot response function
# -----------------------

def rule_based_intent(message):
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

    return None

def chatbot_with_fallback(message, threshold=0.3):

    forced_intent = rule_based_intent(message)
    if forced_intent:
        conversation_context["last_intent"] = forced_intent
        response = reponses.get(forced_intent, reponses["unknown"])
        if isinstance(response, list):
            return random.choice(response)
        return response

    message_clean = nettoyer(message)
    vect = vectorizer.transform([message_clean])

    proba = model.predict_proba(vect)[0]
    max_prob = max(proba)
    intention = model.classes_[proba.argmax()]

    if max_prob < threshold:
        if conversation_context["last_intent"]:
            intention = conversation_context["last_intent"]
        else:
            return reponses["unknown"]

    conversation_context["last_intent"] = intention
    response = reponses.get(intention, reponses["unknown"])

    if isinstance(response, list):
        return random.choice(response)

    return response


def chatbot_enhanced(message,threshold=0.3):

    conversation_context["last_intent"] = None
    responses = []

    email_response = handle_email(message)
    if email_response:
        return email_response
    recall = handle_email_recall(message)
    if recall:
        return recall

    
    questions = re.split(r'[?.!]| et |,', message)
    questions = [q.strip() for q in questions if q.strip()]

    for q in questions:
        date_time_response = handle_datetime(q)
        if date_time_response:
            responses.append(date_time_response)
            continue
        bye_response=handle_goodbye(q)
        if bye_response:
            responses.append(bye_response)
            continue
        calcul = calc(q)
        if calcul:
            responses.append(calcul)
            continue
        else:
            responses.append(chatbot_with_fallback(q, threshold))

    return " ".join(responses)




