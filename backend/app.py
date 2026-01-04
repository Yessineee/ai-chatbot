# app.py

from flask import Flask, request, jsonify,Response
from flask_cors import CORS
from session_manager import SessionManager
from model import chatbot_enhanced
import logging
import uuid
from datetime import datetime
from functools import wraps
import os

# Set up logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    handlers=[logging.FileHandler('chatbot.log') ,logging.StreamHandler()],
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration from environment variables
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
MAX_MESSAGE_LENGTH = int(os.getenv('MAX_MESSAGE_LENGTH', '1000'))
API_VERSION = "1.0.0"
SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT_MINUTES', '30'))
session_manager = SessionManager(session_timeout_minutes=SESSION_TIMEOUT)


ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 
    'http://localhost:5173,http://localhost:3000'
).split(',')

if ENVIRONMENT == 'production':
    # Strict CORS, no debug logs
    logger.info(f"Production mode - CORS restricted to: {ALLOWED_ORIGINS}")
    CORS(app, resources={
        r"/*": {
            "origins": ALLOWED_ORIGINS,
            "methods": ["GET", "POST", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
else:
    logger.info("Development mode - CORS allowing all origins")
    CORS(app)  # Allow all in development
    

def validate_request(required_fields=None):
    
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Check content type
            if not request.is_json:
                return jsonify({
                    "error": "Content-Type must be application/json"
                }), 400

            data = request.get_json()
            if not isinstance(data, dict):
                return jsonify({
                    "error": "Invalid JSON format"
                }), 400

            # Check required fields
            if required_fields:
                missing = [field for field in required_fields if field not in data]
                if missing:
                    return jsonify({
                        "error": f"Missing required fields: {', '.join(missing)}"
                    }), 400

            from flask import g
            g.validated_data = data

            return f(*args, **kwargs)

        return wrapper

    return decorator


def handle_errors(f):
    
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Validation error: {e}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Unexpected error in {f.__name__}: {e}", exc_info=True)
            return jsonify({
                "error": "Internal server error",
                "message": "Une erreur inattendue s'est produite."
            }), 500

    return wrapper




def extract_name(message):
    """Extract user's name from their message."""
    message_clean = message.lower().strip()

    # Remove common phrases
    patterns_to_remove = [
        r"my name is ", r"i am ", r"i'm ", r"call me ",
        r"it's ", r"this is ", r"je m'appelle ", r"je suis ",
        r"c'est ", r"mon nom est "
    ]

    for pattern in patterns_to_remove:
        message = re.sub(pattern, "", message_clean, flags=re.IGNORECASE)

    # Clean up
    message_clean = re.sub(r"[^\w\s]", "", message_clean).strip()
    if not message_clean:
        message_clean = re.sub(r"[^\w\s]", "", message).strip()

    # Extract name
    words = message_clean.split()
    if len(words) == 1:
        return words[0].capitalize()
    elif len(words) == 2:
        return " ".join([w.capitalize() for w in words])
    elif len(words) > 0:
        return words[0].capitalize()

    return message.strip().capitalize() if message.strip() else None


def personalize_response(response, user_name):
    
    if not user_name:
        return response

    # Add name to certain responses
    personalizations = {
        "Bonjour": f"Bonjour {user_name}",
        "Hello!": f"Hello {user_name}!",
        "Hi there!": f"Hi {user_name}!",
        "Avec plaisir": f"Avec plaisir {user_name}",
        "You're welcome!": f"You're welcome, {user_name}!",
    }

    for original, personalized in personalizations.items():
        if original in response:
            response = response.replace(original, personalized)
            break

    return response






@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Chatbot API",
        "version": API_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route('/health', methods=['GET'])
def health():
    from model import vectorizer, model
    
    """Detailed health check"""
    model_exists = os.path.exists('models/chatbot_model.pkl')
    model_loaded = (vectorizer is not None and model is not None)
    stats = session_manager.get_stats()
    return jsonify({
        "status": "healthy",
        "version": API_VERSION,
        "model_exists_on_disk": model_exists,
        "model_loaded_in_memory": model_loaded,
        "sessions": stats,
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route('/start', methods=['POST'])
@handle_errors
def start_conversation():
   
    # Create new session
    session_id = session_manager.create_session()
    logger.info(f"Started new conversation: {session_id}")

    # Get the session to verify it was created
    session = session_manager.get_session(session_id)
    logger.info(f"Session after creation - name_asked: {session.get('name_asked')}, user_name: {session.get('user_name')}")

    # IMPORTANT: Mark that we're asking for the name
    result=session_manager.update_session(session_id, name_asked=True)
    logger.info(f"Update session result: {result}")

    # Verify the update worked
    session = session_manager.get_session(session_id)
    logger.info(f"Session after update - name_asked: {session.get('name_asked')}, user_name: {session.get('user_name')}")

    # Return greeting that asks for name
    greeting = "Hello! 👋 I'm your AI assistant. What should I call you?"

    return jsonify({
        "response": greeting,
        "session_id": session_id,
        "ask_for_name": True,
        "timestamp": datetime.utcnow().isoformat()
    })




@app.route('/chat', methods=['POST'])
@handle_errors
@validate_request(required_fields=['message'])
def chat():

    from flask import g
    data = g.validated_data

    # Get or create session
    session_id = data.get('session_id')
    if not session_id:
        session_id = session_manager.create_session()
        logger.info(f"Created new session: {session_id}")

    # Get session data (read-only reference)
    session = session_manager.get_session(session_id)
    if not session:
        logger.error(f"Failed to get session: {session_id}")
        return jsonify({"error": "Invalid session"}), 400

    # Get message
    message = data.get('message', '').strip()

    # Validate message
    if not message:
        return jsonify({
            "error": "Message cannot be empty",
            "session_id": session_id
        }), 400

    if len(message) > MAX_MESSAGE_LENGTH:
        return jsonify({
            "error": f"Message too long (max {MAX_MESSAGE_LENGTH} characters)",
            "session_id": session_id
        }), 400

    # DEBUG: Log session state
    logger.info(f"Session state - name_asked: {session.get('name_asked')}, user_name: {session.get('user_name')}")
    logger.info(f"Received message: {message}")

    if session.get("name_asked") is True and session.get("user_name") is None:
        logger.info("Processing message as name input")
        # This is their response to "What should I call you?"
        # Extract name from their message
        name = extract_name(message)
        if name:
            logger.info(f"Extracted name: {name}")
    
            success=session_manager.update_session(session_id, user_name=name)
            logger.info(f"Update session result: {success}")
            response = f"Nice to meet you, {name}! 😊 How can I help you today?"
            detected_intent = "name_introduction"
    
            # Save to history
            session_manager.add_to_history(session_id, message, response, intent=detected_intent)
    
            return jsonify({
                "response": response,
                "session_id": session_id,
                "intent": detected_intent,
                "user_name": name,
                "timestamp": datetime.utcnow().isoformat()
            })
        else:
            logger.warning(f"Could not extract name from: {message}")
            # If we can't extract a name, use the message as-is
            name = message.capitalize()
            session_manager.update_session(session_id, user_name=name)
            response = f"Nice to meet you, {name}! 😊 How can I help you today?"
            detected_intent = "name_introduction"
            
            session_manager.add_to_history(session_id, message, response, intent=detected_intent)
            
            return jsonify({
                "response": response,
                "session_id": session_id,
                "intent": detected_intent,
                "user_name": name,
                "timestamp": datetime.utcnow().isoformat()
            })

    # Normal chat flow - name already set
    logger.info(f"Processing as normal chat message")


    
    logger.info(f"Session {session_id[:8]}... received message: {message[:50]}...")
    
    try:
        response, detected_intent, email_extracted = chatbot_enhanced(message,session,threshold=0.2)
        user_name = session.get("user_name")
        
        if user_name and detected_intent in ["greeting", "thanks"]:
            response = personalize_response(response, user_name)

    except Exception as e:
        logger.error(f"Error getting chatbot response: {e}", exc_info=True)
        response = "Désolé, une erreur s'est produite. Veuillez réessayer."
        detected_intent = None
        email_extracted = None

    # Update session through session_manager 
    updates = {}
    if detected_intent:
        updates['last_intent'] = detected_intent
    if email_extracted:
        updates['email'] = email_extracted

    if updates:

        session_manager.update_session(session_id, **updates)

        logger.debug(f"Updated session {session_id[:8]}... with: {updates}")

    # Save conversation to history
    session_manager.add_to_history(session_id, message,response,intent=detected_intent)

    logger.info(f"Session {session_id[:8]}... response: {response[:50]}... (intent: {detected_intent})")

    return jsonify({
        "response": response,
        "session_id": session_id,
        "intent": detected_intent,
        "user_name": session.get("user_name"),
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route('/history/<session_id>', methods=['GET'])
@handle_errors
def get_history(session_id):
    limit = request.args.get('limit', 10, type=int)

    # Validate limit
    if limit < 1 or limit > 100:
        return jsonify({"error": "Limit must be between 1 and 100"}), 400

    history = session_manager.get_history(session_id, limit=limit)

    return jsonify({
        "history": history,
        "session_id": session_id,
        "count": len(history)
    })


@app.route('/session/<session_id>', methods=['DELETE'])
@handle_errors
def clear_session(session_id):
    success = session_manager.clear_session(session_id)

    if success:
        return jsonify({
            "message": "Session cleared successfully",
            "session_id": session_id
        })
    else:
        return jsonify({
            "message": "Session not found",
            "session_id": session_id
        }), 404


@app.route('/stats', methods=['GET'])
def get_stats():
    stats = session_manager.get_stats()
    return jsonify({
        "stats": stats,
        "version": API_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "message": "The requested URL was not found on the server."
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        "error": "Method not allowed",
        "message": "The method is not allowed for the requested URL."
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}", exc_info=True)
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred."
    }), 500


# Periodic cleanup task (run every hour)
from threading import Thread
import time


def cleanup_task():
    """Background task to cleanup expired sessions"""
    while True:
        try:
            time.sleep(3600)  # Sleep for 1 hour
            expired = session_manager.cleanup_expired_sessions()
            logger.info(f"Cleaned up {expired} expired sessions")
        except Exception as e:
            logger.error(f"Error in cleanup task: {e}")


# Start cleanup thread
cleanup_thread = Thread(target=cleanup_task, daemon=True)
cleanup_thread.start()

if __name__ == '__main__':
    logger.info("Starting chatbot server...")
    logger.info(f"API Version: {API_VERSION}")
    app.run(debug=True, host='0.0.0.0', port=5000)















