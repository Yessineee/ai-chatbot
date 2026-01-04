import { useState } from "react";
import { Bot, Sparkles, ArrowRight } from "lucide-react";

interface WelcomeNamePageProps {
  onNameSubmit: (name: string) => void;
}

const WelcomeNamePage = ({ onNameSubmit }: WelcomeNamePageProps) => {
  const [name, setName] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (name.trim()) {
      setIsSubmitting(true);
      // Small delay for smooth transition
      setTimeout(() => {
        onNameSubmit(name.trim());
      }, 300);
    }
  };

  const handleSkip = () => {
    setIsSubmitting(true);
    setTimeout(() => {
      onNameSubmit("Guest");
    }, 300);
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-primary/5 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-accent/5 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-primary/3 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }}></div>
      </div>

      <div className="max-w-md w-full relative z-10">
        {/* Logo/Bot Icon */}
        <div className="text-center mb-8 animate-fade-in">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-primary/20 to-accent/20 border border-primary/20 mb-4 relative">
            <Bot className="w-10 h-10 text-primary" />
            <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-emerald-500 rounded-full border-2 border-background animate-pulse" />
          </div>
          <h1 className="text-3xl font-bold text-foreground mb-2 flex items-center justify-center gap-2">
            AI Assistant
            <Sparkles className="w-6 h-6 text-primary animate-pulse" />
          </h1>
          <p className="text-muted-foreground">
            Your intelligent conversation partner
          </p>
        </div>

        {/* Welcome Card */}
        <div 
          className={`bg-card/50 backdrop-blur-sm border border-border rounded-2xl p-8 shadow-xl transition-all duration-300 ${
            isSubmitting ? 'opacity-0 scale-95' : 'opacity-100 scale-100'
          }`}
        >
          <div className="mb-6">
            <h2 className="text-2xl font-semibold text-foreground mb-2">
              Welcome! 👋
            </h2>
            <p className="text-muted-foreground">
              What should I call you?
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter your name..."
                className="w-full px-4 py-3 bg-background border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50 text-foreground placeholder:text-muted-foreground transition-all"
                autoFocus
                maxLength={50}
                disabled={isSubmitting}
              />
              <p className="text-xs text-muted-foreground mt-2">
                This helps me personalize our conversation
              </p>
            </div>

            <div className="flex gap-3">
              <button
                type="submit"
                disabled={!name.trim() || isSubmitting}
                className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-gradient-to-r from-primary to-accent text-primary-foreground rounded-xl font-medium hover:shadow-lg hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
              >
                Continue
                <ArrowRight className="w-4 h-4" />
              </button>
              
              <button
                type="button"
                onClick={handleSkip}
                disabled={isSubmitting}
                className="px-6 py-3 bg-secondary text-secondary-foreground rounded-xl font-medium hover:bg-secondary/80 transition-all duration-200 disabled:opacity-50"
              >
                Skip
              </button>
            </div>
          </form>

          {/* Features */}
          <div className="mt-8 pt-6 border-t border-border">
            <p className="text-xs text-muted-foreground mb-3">I can help you with:</p>
            <div className="grid grid-cols-2 gap-2">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <span className="w-1.5 h-1.5 rounded-full bg-primary"></span>
                <span>General questions</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <span className="w-1.5 h-1.5 rounded-full bg-primary"></span>
                <span>Information search</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <span className="w-1.5 h-1.5 rounded-full bg-primary"></span>
                <span>Calculations</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <span className="w-1.5 h-1.5 rounded-full bg-primary"></span>
                <span>And much more...</span>
              </div>
            </div>
          </div>
        </div>

        {/* Footer note */}
        <p className="text-center text-xs text-muted-foreground mt-6">
          Press Enter to continue or click Skip to start as Guest
        </p>
      </div>
    </div>
  );
};

export default WelcomeNamePage;