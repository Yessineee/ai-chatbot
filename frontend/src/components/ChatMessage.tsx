import { Bot, User, Copy, RotateCcw, ThumbsUp, ThumbsDown, Check } from "lucide-react";
import { useState } from "react";

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  isNew?: boolean;
}

const ChatMessage = ({ message, isUser, isNew }: ChatMessageProps) => {
  const [copied, setCopied] = useState(false);
  const [feedback, setFeedback] = useState<'up' | 'down' | null>(null);

  const handleCopy = () => {
    navigator.clipboard.writeText(message);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleFeedback = (type: 'up' | 'down') => {
    setFeedback(type);
    // Here you could send feedback to your backend
  };

  return (
    <div
      className={`flex gap-4 ${isUser ? "justify-end" : "justify-start"} ${
        isNew ? "animate-fade-in" : ""
      } group`}
    >
      {!isUser && (
        <div className="flex-shrink-0">
          <div className="w-10 h-10 rounded-full bg-teal-500/20 border border-teal-500/30 flex items-center justify-center">
            <Bot className="w-5 h-5 text-teal-500" />
          </div>
        </div>
      )}

      <div className="flex flex-col gap-2 max-w-[80%]">
        <div
          className={`rounded-2xl px-5 py-3 ${
            isUser
              ? "bg-teal-600 text-white"
              : "bg-gray-800 text-gray-100 border border-gray-700"
          }`}
        >
          <p className="whitespace-pre-wrap break-words leading-relaxed">
            {message}
          </p>
        </div>

        {/* Action buttons for AI messages */}
        {!isUser && (
          <div className="flex gap-2 px-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
            <button
              onClick={handleCopy}
              className="p-2 rounded-lg hover:bg-gray-800 transition-colors"
              title="Copier"
            >
              {copied ? (
                <Check className="w-4 h-4 text-green-500" />
              ) : (
                <Copy className="w-4 h-4 text-gray-400 hover:text-gray-300" />
              )}
            </button>
            
            <button
              onClick={() => handleFeedback('up')}
              className={`p-2 rounded-lg hover:bg-gray-800 transition-colors ${
                feedback === 'up' ? 'bg-gray-800' : ''
              }`}
              title="Bonne réponse"
            >
              <ThumbsUp className={`w-4 h-4 ${
                feedback === 'up' ? 'text-teal-500' : 'text-gray-400 hover:text-gray-300'
              }`} />
            </button>
            
            <button
              onClick={() => handleFeedback('down')}
              className={`p-2 rounded-lg hover:bg-gray-800 transition-colors ${
                feedback === 'down' ? 'bg-gray-800' : ''
              }`}
              title="Mauvaise réponse"
            >
              <ThumbsDown className={`w-4 h-4 ${
                feedback === 'down' ? 'text-red-500' : 'text-gray-400 hover:text-gray-300'
              }`} />
            </button>
          </div>
        )}
      </div>

      {isUser && (
        <div className="flex-shrink-0">
          <div className="w-10 h-10 rounded-full bg-gray-700 border border-gray-600 flex items-center justify-center">
            <User className="w-5 h-5 text-gray-300" />
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatMessage;