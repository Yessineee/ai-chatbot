import unicodedata
from datetime import datetime
from data import time,bye
import random
import re

conversation_context = {
    "last_intent": None,
    "email": None
}


def normalize_text(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()





def handle_email_recall(message):
    msg = normalize_text(message)

    if any(expr in msg for expr in [
        "what is my email", "quel est mon email", "mon email"
    ]):
        if conversation_context.get("email"):
            return f"Votre email est : {conversation_context['email']}"
        else:
            return "Je n’ai pas encore votre email. Vous pouvez me le donner 😊"

    return None

def handle_goodbye(message):
    msg=message.lower()
    hour = datetime.now().hour

    if 5 <= hour < 12:
        greeting = "Bonne matinée"
    elif 12 <= hour < 18:
        greeting = "Bon après-midi"
    elif 18 <= hour < 22:
        greeting = "Bonne soirée"
    else:
        greeting = "Bonne nuit"

    suffixes = [
        "!",
        ", à bientôt !",
        " et au plaisir de te revoir.",
        ". J'espère avoir pu t'aider !"
    ]
    if any(word in msg for word in bye):
        return f"{greeting}{random.choice(suffixes)}"

    return None

def handle_datetime(message):
    msg = message.lower()

    if any(word in msg for word in time):
        return f"Il est {datetime.now().strftime('%H:%M')}."

    if "date" in msg or "aujourd'hui" in msg:
        return f"Nous sommes le {datetime.now().strftime('%d/%m/%Y')}."

    return None


def handle_email(message):
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    match = re.search(email_pattern, message)

    if match:
        email = match.group()
        conversation_context["email"] = email
        return f"Merci, j’ai bien enregistré votre email : {email}"

    return None