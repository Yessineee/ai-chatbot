import { useState, useRef, useEffect } from "react";
import ChatHeader from "./ChatHeader";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
import TypingIndicator from "./TypingIndicator";
import WelcomeScreen from "./WelcomeScreen";
import { set } from "date-fns";
// import SuggestedPrompts from "./SuggestedPrompts";

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  isNew?: boolean;
  intent?: string;
}

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";


const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      text: "Bonjour ! Je suis votre assistant IA. Comment puis-je vous aider aujourd'hui ?",
      isUser: false,
    },
    
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Check if this is the first message (welcome state)
  const isWelcomeState = messages.length === 1 && !messages[0].isUser;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  // Load session ID from localStorage on mount
  useEffect(() => {
    const savedSessionId = localStorage.getItem("chatbot_session_id");
    if (savedSessionId) {
      setSessionId(savedSessionId);
      console.log("Loaded existing session:", savedSessionId.substring(0, 8) + "...");
    }
  }, []);

  // Save session ID to localStorage whenever it changes
  useEffect(() => {
    if (sessionId) {
      localStorage.setItem("chatbot_session_id", sessionId);
      console.log("Saved session:", sessionId.substring(0, 8) + "...");
    }
  }, [sessionId]);


  const handleSend = async (text: string) => {
    // Clear any previous errors
    setError(null);

     // Validate input
    if (!text.trim()) {
      return;
    }

    if (text.length > 1000) {
      setError("Message trop long (maximum 1000 caractères)");
      return;
    }

    const userMessage: Message = {
      id: Date.now().toString(),
      text,
      isUser: true,
      isNew: true,
    };

    setMessages((prev) => [
      ...prev.map((m) => ({ ...m, isNew: false })),
      userMessage,
    ]);

    
    setIsTyping(true);

    try {

      console.log("Sending message:", text.substring(0, 50) + "...");
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: text, session_id: sessionId }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

      // Save session ID from response (first message or new session)
      if (data.session_id && !sessionId) {
        setSessionId(data.session_id);
        console.log("Received new session:", data.session_id.substring(0, 8) + "...");
      }
    
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: data.response,
        isUser: false,
        isNew: true,
        intent: data.intent,
      };
      console.log("Received response. Intent:", data.intent);

      setMessages((prev) => [
        ...prev.map((m) => ({ ...m, isNew: false })),
        aiResponse,
      ]);
    } catch (error) {
      console.error("Error sending message:", error);
      
      let errorText = "Erreur de connexion au serveur.";

       if (error instanceof Error) {
        if (error.message.includes("Failed to fetch")) {
          errorText = "Impossible de se connecter au serveur. Vérifiez votre connexion.";
        } else {
          errorText = `Erreur: ${error.message}`;
        }
      }

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "Erreur de connexion au serveur.",
        isUser: false,
        isNew: true,
      };

      setMessages((prev) => [...prev, errorMessage]);
      setError(errorText);
    } finally {
      setIsTyping(false);
    }
  };

   // Clear conversation (and session)
  const handleClearChat = () => {
    if (window.confirm("Voulez-vous vraiment effacer la conversation ?")) {
      // Clear session on backend
      if (sessionId) {
        fetch(`${API_BASE_URL}/session/${sessionId}`, {
          method: "DELETE",
        }).catch((error) => {
          console.error("Error clearing session:", error);
        });
      }

      // Clear local state
      setMessages([
        {
          id: "1",
          text: "Bonjour ! Je suis votre assistant IA. Comment puis-je vous aider aujourd'hui ?",
          isUser: false,
        },
      ]);
      setSessionId(null);
      localStorage.removeItem("chatbot_session_id");
      setError(null);
      
      console.log("Chat cleared");
    }
  };

  // const handleSuggestedPrompt = (prompt: string) => {
  //   handleSend(prompt);
  // };

  return (
    <div className="flex flex-col h-screen bg-background relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-teal-500/5 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      <ChatHeader onClearChat={handleClearChat} />
      
      <main className="flex-1 overflow-y-auto scrollbar-thin relative z-10">
        <div className="max-w-3xl mx-auto px-4 py-6 space-y-6">
           {/* Show error message if any */}
          {error && (
            <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-4 text-red-400 text-sm">
              {error}
            </div>
          )}

          {/* Session ID indicator (for debugging - can remove in production) */}
          {sessionId && import.meta.env.DEV && (
            <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-2 text-blue-400 text-xs text-center">
              Session: {sessionId.substring(0, 8)}...
            </div>
          )}


          {/* Show welcome screen only on first load */}
          {isWelcomeState && <WelcomeScreen />}
          
          {messages.map((message) => (
            <ChatMessage
              key={message.id}
              message={message.text}
              isUser={message.isUser}
              isNew={message.isNew}
            />
          ))}
          
          {isTyping && <TypingIndicator />}
          
          {/* Show suggested prompts after first AI response
          {!isTyping && messages.length >= 2 && (
            <SuggestedPrompts onPromptClick={handleSuggestedPrompt} />
          )} */}
          
          <div ref={messagesEndRef} />
        </div>
      </main>

      <ChatInput onSend={handleSend} disabled={isTyping} />
    </div>
  );
};

export default ChatInterface;
