import { Bot } from "lucide-react";

const TypingIndicator = () => {
  return (
    <div className="flex gap-4 animate-fade-in-up">
      <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-chat-ai-border text-primary">
        <Bot className="w-4 h-4" />
      </div>
      <div className="bg-chat-ai border border-chat-ai-border rounded-2xl rounded-tl-sm px-4 py-3">
        <div className="flex gap-1.5 items-center h-5">
          <span className="w-2 h-2 rounded-full bg-primary animate-pulse-dot" />
          <span className="w-2 h-2 rounded-full bg-primary animate-pulse-dot-delay-1" />
          <span className="w-2 h-2 rounded-full bg-primary animate-pulse-dot-delay-2" />
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;
