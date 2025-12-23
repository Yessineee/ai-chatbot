import { Bot, Sparkles } from "lucide-react";
import { ThemeToggle } from "./ThemeToggle";

const ChatHeader = () => {
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
          <p className="text-xs text-muted-foreground">Always here to help</p>
        </div>
        <ThemeToggle />
      </div>
    </header>
  );
};

export default ChatHeader;
