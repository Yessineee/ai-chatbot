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
    import wikipedia
    try:
        msg = message.lower().strip()
        # Detect Wikipedia search intent
        patterns = [
            r"(?:search|look up|find|tell me about|what is|who is|explain)\s+(?:on\s+)?(?:wikipedia\s+)?(?:for\s+)?(.+)",
            r"wikipedia\s+(.+)",
            r"(?:information|info)\s+(?:about|on)\s+(.+)"
            r"search (?:wikipedia |wiki )?for (.+)",
            r"look up (.+) (?:on |in )?(?:wikipedia|wiki)",
            r"what is (.+)",
            r"who is (.+)",
            r"tell me about (.+)",
            r"find (?:information )?(?:about |on )?(.+)",
            r"wikipedia (.+)",
            r"wiki (.+)",
            r"(?:search|find|cherche) (.+)",
            r"recherche (.+)",
            r"qui est (.+)",
            r"c'est quoi (.+)",
        ]

        search_query = None
        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                search_query = match.group(1).strip()
                break
        # If no pattern matched, check if it's a simple "what is X" type question
        if not search_query and msg.startswith(("what is ", "who is ", "tell me about ", "qui est ", "c'est quoi ")):
            parts = msg.split(None, 2)  # Split into max 3 parts
            if len(parts) >= 3:
                search_query = parts[2]

        if not search_query:
            return None

        # Clean up the query
        search_query = search_query.strip('?.,!').strip()

        # Filter out very short or meaningless queries
        if len(search_query) < 2 or search_query in ['it', 'that', 'this', 'you', 'me', 'ça', 'cela']:
            return None

        logger.info(f"Wikipedia search for: {search_query}")

        # Try English first, then French
        languages = ['en', 'fr']

        # Search Wikipedia
        for lang in languages:
            try:
                wikipedia.set_lang(lang)
                logger.debug(f"Trying language: {lang}")

                # First, try to search for the topic
                search_results = wikipedia.search(search_query, results=5)

                if not search_results:
                    logger.debug(f"No results in {lang}")
                    continue

                logger.info(f"Found {len(search_results)} results in {lang}: {search_results}")

                # Try each search result until one works
                for result in search_results:
                    try:
                        logger.debug(f"Attempting to fetch: {result}")

                        # Get the page
                        page = wikipedia.page(result, auto_suggest=False)

                        # Get summary (3 sentences)
                        summary = wikipedia.summary(result, sentences=3, auto_suggest=False)

                        # Format the response
                        response = f"📚 **{page.title}**\n\n{summary}\n\n🔗 En savoir plus : {page.url}"

                        logger.info(f"Successfully fetched: {page.title}")
                        return response

                    except wikipedia.exceptions.DisambiguationError as e:
                        # Multiple possibilities found - try the first option
                        logger.debug(f"Disambiguation error for '{result}', trying first option")
                        if e.options:
                            try:
                                first_option = e.options[0]
                                logger.debug(f"Trying disambiguation option: {first_option}")
                                page = wikipedia.page(first_option, auto_suggest=False)
                                summary = wikipedia.summary(first_option, sentences=3, auto_suggest=False)

                                response = f"📚 **{page.title}**\n\n{summary}\n\n🔗 En savoir plus : {page.url}"
                                logger.info(f"Successfully fetched via disambiguation: {page.title}")
                                return response
                            except:
                                # If first option fails, continue to next result
                                continue

                    except wikipedia.exceptions.PageError:
                        # This page doesn't exist, try next result
                        logger.debug(f"PageError for '{result}', trying next")
                        continue

                    except Exception as e:
                        # Any other error, try next result
                        logger.debug(f"Error fetching '{result}': {e}")
                        continue

            except Exception as e:
                logger.debug(f"Error in {lang} search: {e}")
                continue

            # If we get here, nothing worked
        logger.warning(f"Could not find Wikipedia article for: {search_query}")
        return f"Je n'ai pas trouvé d'article Wikipedia clair pour '{search_query}'. Essayez d'être plus précis ou utilisez un autre terme."

    except Exception as e:
        logger.error(f"Error in handle_wikipedia_search: {e}", exc_info=True)
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


