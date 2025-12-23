import { useState, useRef, useEffect } from "react";
import ChatHeader from "./ChatHeader";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
import TypingIndicator from "./TypingIndicator";
import WelcomeScreen from "./WelcomeScreen";
// import SuggestedPrompts from "./SuggestedPrompts";

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  isNew?: boolean;
}

const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      text: "Bonjour ! Je suis votre assistant IA. Comment puis-je vous aider aujourd'hui ?",
      isUser: false,
    },
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Check if this is the first message (welcome state)
  const isWelcomeState = messages.length === 1 && !messages[0].isUser;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = async (text: string) => {
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
      const response = await fetch("https://ai-chatbot-1-8fde.onrender.com/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: text }),
      });

      const data = await response.json();

      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: data.response,
        isUser: false,
        isNew: true,
      };

      setMessages((prev) => [
        ...prev.map((m) => ({ ...m, isNew: false })),
        aiResponse,
      ]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "Erreur de connexion au serveur.",
        isUser: false,
        isNew: true,
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
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

      <ChatHeader />
      
      <main className="flex-1 overflow-y-auto scrollbar-thin relative z-10">
        <div className="max-w-3xl mx-auto px-4 py-6 space-y-6">
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
