import unicodedata
from datetime import datetime
from data import time,bye
import random
import re
import logging



logger = logging.getLogger(__name__)

def normalize_text(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()



def handle_wikipedia_search(message):
    try:
        import wikipedia
        # Detect Wikipedia search intent
        patterns = [
            r"(?:search|look up|find|tell me about|what is|who is|explain)\s+(?:on\s+)?(?:wikipedia\s+)?(?:for\s+)?(.+)",
            r"wikipedia\s+(.+)",
            r"(?:information|info)\s+(?:about|on)\s+(.+)"
        ]

        query = None
        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                query = match.group(1).strip()
                break

        if not query:
            return None

        logger.info(f"Wikipedia search for: {query}")

        # Search Wikipedia
        try:
            # Get summary (first 3 sentences)
            summary = wikipedia.summary(query, sentences=3)

            # Get page URL
            page = wikipedia.page(query)
            url = page.url

            response = f"{summary}\n\nSource: {url}"
            return response

        except wikipedia.exceptions.DisambiguationError as e:
            # Multiple results found
            options = e.options[:5]  # Show first 5 options
            return f"Plusieurs résultats trouvés pour '{query}'. Voulez-vous dire: {', '.join(options)}?"

        except wikipedia.exceptions.PageError:
            return f"Désolé, je n'ai pas trouvé d'article Wikipedia pour '{query}'. Essayez un autre terme."

        except Exception as e:
            logger.error(f"Wikipedia search error: {e}")
            return f"Une erreur s'est produite lors de la recherche. Réessayez avec un terme différent."

    except ImportError:
        logger.warning("Wikipedia module not installed")
        return "La recherche Wikipedia n'est pas disponible. Installez: pip install wikipedia"

    except Exception as e:
        logger.error(f"Error in handle_wikipedia_search: {e}")
        return None


def handle_email_recall(message,session):

    msg = normalize_text(message)

    if any(expr in msg for expr in [
        "what is my email", "quel est mon email", "mon email",
        "my email", "rappelle mon email", "recall my email"
    ]):

        email = session.get("email")
        if email:
            return f"Votre email est : {email}"
        else:
            return "Je n'ai pas encore votre email. Vous pouvez me le donner 😊"

        # if conversation_context.get("email"):
        #     return f"Votre email est : {conversation_context['email']}"
        # else:
        #     return "Je n’ai pas encore votre email. Vous pouvez me le donner 😊"

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
        confirmation=f"Merci, j’ai bien enregistré votre email : {email}"
        return confirmation,email

    return None,None

def validate_email(email):

    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None
