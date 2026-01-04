import { Bot, Sparkles, Trash2,User } from "lucide-react";
import { ThemeToggle } from "./ThemeToggle";


interface ChatHeaderProps {
  onClearChat?: () => void;
  userName?: string | null;
}

const ChatHeader = ({ onClearChat, userName }: ChatHeaderProps) => {
  return (
    <header className="border-b border-border bg-card/50 backdrop-blur-sm px-6 py-4">
      <div className="max-w-3xl mx-auto flex items-center gap-3">
        <div className="relative">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary/20 to-accent/20 flex items-center justify-center border border-primary/20">
            <Bot className="w-5 h-5 text-primary" />
          </div>
          <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-emerald-500 rounded-full border-2 border-background" />
        </div>
        <div className="flex-1">
          <h1 className="text-foreground font-semibold flex items-center gap-2">
            AI Assistant
            <Sparkles className="w-4 h-4 text-primary" />
          </h1>
          <p className="text-xs text-muted-foreground">{userName ? `Chatting with ${userName}` : "Always here to help"}</p>
        </div>

        {/* User name badge */}
        {userName && (
          <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-primary/10 border border-primary/20">
            <User className="w-3.5 h-3.5 text-primary" />
            <span className="text-sm text-foreground">{userName}</span>
          </div>
        )}
        
        {onClearChat && (
          <button
            onClick={onClearChat}
            className="flex items-center gap-2 px-3 py-2 rounded-lg bg-red-500/10 hover:bg-red-500/20 border border-red-500/20 text-red-400 hover:text-red-300 transition-all duration-200 text-sm"
            title="Effacer la conversation"
          >
            <Trash2 className="w-4 h-4" />
            <span className="hidden sm:inline">Clear</span>
          </button>
        )}
        <ThemeToggle />
      </div>
    </header>
  );
};

export default ChatHeader;
