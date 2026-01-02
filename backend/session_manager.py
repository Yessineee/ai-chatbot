"""
Session Manager for Chatbot
Handles per-user conversation context and state
"""

from datetime import datetime, timedelta
import uuid
import threading
from typing import Dict, Optional


class SessionManager:
    """
    Manages user sessions and conversation context.
    Each user gets their own isolated context.
    """

    def __init__(self, session_timeout_minutes: int = 30):
        """
        Initialize the session manager.

        Args:
            session_timeout_minutes: How long before a session expires
        """
        self.sessions: Dict[str, Dict] = {}
        self.session_timeout = timedelta(minutes=session_timeout_minutes)
        self.lock = threading.RLock()  # Thread-safe operations


    def create_session(self) -> str:
        """
        Create a new session and return its ID.

        Returns:
            str: Unique session ID
        """
        session_id = str(uuid.uuid4())

        with self.lock:
            self.sessions[session_id] = {
                "last_intent": None,
                "email": None,
                "conversation_history": [],
                "created_at": datetime.now(),
                "last_activity": datetime.now()
            }

        return session_id


    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        Get session data for a user.
        Creates new session if it doesn't exist or expired.

        Args:
            session_id: The session identifier

        Returns:
            dict: Session data or None if invalid
        """
        with self.lock:
            # Check if session exists
            if session_id not in self.sessions:
                # Create new session with this ID
                self.sessions[session_id] = {
                    "last_intent": None,
                    "email": None,
                    "conversation_history": [],
                    "created_at": datetime.now(),
                    "last_activity": datetime.now()
                }
                return self.sessions[session_id]

            session = self.sessions[session_id]

            # Check if session expired
            if datetime.now() - session["last_activity"] > self.session_timeout:
                # Session expired, create new one
                self.sessions[session_id] = {
                    "last_intent": None,
                    "email": None,
                    "conversation_history": [],
                    "created_at": datetime.now(),
                    "last_activity": datetime.now()
                }
                return self.sessions[session_id]

            # Update last activity
            session["last_activity"] = datetime.now()
            return session

    def update_session(self, session_id: str, **kwargs) -> bool:
        """
        Update session data.

        Args:
            session_id: The session identifier
            **kwargs: Key-value pairs to update (email, last_intent, etc.)

        Returns:
            bool: True if successful, False otherwise
        """
        with self.lock:
            session = self.get_session(session_id)
            if not session:
                return False

            # Update allowed fields
            allowed_fields = ["last_intent", "email"]
            for key, value in kwargs.items():
                if key in allowed_fields:
                    session[key] = value

            session["last_activity"] = datetime.now()
            return True

    def add_to_history(self, session_id: str, user_message: str,
                       bot_response: str, intent: str = None) -> bool:
        """
        Add a conversation exchange to history.

        Args:
            session_id: The session identifier
            user_message: What the user said
            bot_response: What the bot replied
            intent: Detected intent (optional)

        Returns:
            bool: True if successful
        """
        with self.lock:
            session = self.get_session(session_id)
            if not session:
                return False

            # Add to history (keep last 50 messages)
            session["conversation_history"].append({
                "user": user_message,
                "bot": bot_response,
                "intent": intent,
                "timestamp": datetime.now().isoformat()
            })

            # Keep only last 50 exchanges
            if len(session["conversation_history"]) > 50:
                session["conversation_history"] = session["conversation_history"][-50:]

            return True

    def get_history(self, session_id: str, limit: int = 10) -> list:
        """
        Get conversation history for a session.

        Args:
            session_id: The session identifier
            limit: Maximum number of messages to return

        Returns:
            list: List of conversation exchanges
        """
        with self.lock:
            session = self.get_session(session_id)
            if not session:
                return []

            history = session.get("conversation_history", [])
            return history[-limit:] if history else []

    def clear_session(self, session_id: str) -> bool:
        """
        Clear/delete a session.

        Args:
            session_id: The session identifier

        Returns:
            bool: True if session was deleted
        """
        with self.lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
                return True
            return False

    def cleanup_expired_sessions(self):
        """
        Remove all expired sessions.
        Should be called periodically (e.g., every hour).
        """
        with self.lock:
            now = datetime.now()
            expired = [
                sid for sid, session in self.sessions.items()
                if now - session["last_activity"] > self.session_timeout
            ]

            for sid in expired:
                del self.sessions[sid]

            return len(expired)

    def get_stats(self) -> Dict:
        """
        Get statistics about active sessions.

        Returns:
            dict: Stats including total sessions, active users, etc.
        """
        with self.lock:
            total = len(self.sessions)
            now = datetime.now()

            active_5min = sum(
                1 for s in self.sessions.values()
                if now - s["last_activity"] < timedelta(minutes=5)
            )

            total_conversations = sum(len(s.get("conversation_history", [])) for s in self.sessions.values())

            return {
                "total_sessions": total,
                "active_last_5min": active_5min,
                "total_conversations": total_conversations,
                "timestamp": now.isoformat()
            }


# Global session manager instance
session_manager = SessionManager(session_timeout_minutes=30)

# Example usage:
if __name__ == "__main__":
    # Create a session
    sid = session_manager.create_session()
    print(f"Created session: {sid}")

    # Update session
    session_manager.update_session(sid, email="user@example.com", last_intent="greeting")

    # Add conversation
    session_manager.add_to_history(sid, "Hello!", "Hi there!", "greeting")

    # Get session data
    session = session_manager.get_session(sid)
    print(f"Session data: {session}")

    # Get history
    history = session_manager.get_history(sid)
    print(f"History: {history}")

    # Get stats
    stats = session_manager.get_stats()
    print(f"Stats: {stats}")