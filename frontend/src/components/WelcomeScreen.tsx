import { MessageSquare, Sparkles, Brain, Zap ,Calculator, Search, Clock,Languages,BookOpen} from "lucide-react";
import { useMemo } from "react";

interface WelcomeScreenProps {
  userName?: string | null;
}

interface FeatureCard {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  description: string;
  iconBgColor: string;
  iconColor: string;
  borderColor: string;
}

const WelcomeScreen = ({ userName }: WelcomeScreenProps) => {
  const features = useMemo<FeatureCard[]>(() => [
    {
      icon: Brain,
      title: "Intelligence Avancée",
      description: "Réponses précises et contextuelles à vos questions",
      iconBgColor: "bg-teal-500/10",
      iconColor: "text-teal-500",
      borderColor: "hover:border-teal-500/30"
    },
    {
      icon: Calculator,
      title: "Calculs Mathématiques",
      description: "Effectuez des calculs et résolvez des équations rapidement",
      iconBgColor: "bg-cyan-500/10",
      iconColor: "text-cyan-500",
      borderColor: "hover:border-cyan-500/30"
    },
    {
      icon: Search,
      title: "Recherche d'Information",
      description: "Accédez à Wikipedia et trouvez des informations fiables",
      iconBgColor: "bg-purple-500/10",
      iconColor: "text-purple-500",
      borderColor: "hover:border-purple-500/30"
    },
    {
      icon: Clock,
      title: "Date & Heure",
      description: "Obtenez l'heure actuelle et des informations temporelles",
      iconBgColor: "bg-blue-500/10",
      iconColor: "text-blue-500",
      borderColor: "hover:border-blue-500/30"
    },
    {
      icon: Languages,
      title: "Multilingue",
      description: "Support complet du français et de l'anglais",
      iconBgColor: "bg-pink-500/10",
      iconColor: "text-pink-500",
      borderColor: "hover:border-pink-500/30"
    },
    {
      icon: Zap,
      title: "Rapidité",
      description: "Réponses instantanées pour une productivité maximale",
      iconBgColor: "bg-amber-500/10",
      iconColor: "text-amber-500",
      borderColor: "hover:border-amber-500/30"
    }
  ], []);

  // Personalized greeting message
  const greetingMessage = useMemo(() => {
    if (userName) {
      return `Bienvenue, ${userName} ! 👋`;
    }
    return "Bienvenue ! 👋";
  }, [userName]);

  return (
    <div className="flex flex-col items-center justify-center py-12 animate-fade-in">
      {/* Main Icon with glow effect */}
      <div className="relative mb-8">

        <div className="absolute inset-0 bg-teal-500/20 rounded-full blur-2xl animate-pulse"></div>
        <div className="absolute inset-0 bg-cyan-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}/>
        {/* Icon container */}
        <div className="relative bg-gradient-to-br from-teal-500/10 to-cyan-500/10 p-8 rounded-full border border-teal-500/20 backdrop-blur-sm">
          <MessageSquare className="w-16 h-16 text-teal-500" />
        </div>
      </div>

      {/* Welcome text with personalization */}
      <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-3 text-center">
        {greetingMessage}
      </h2>

      <p className="text-muted-foreground text-center max-w-md mb-4">
        Votre assistant IA intelligent pour répondre à vos questions et vous aider dans vos tâches
      </p>

       {/* Quick tips */}
      <div className="flex items-center gap-2 text-sm text-muted-foreground mb-12">
        <BookOpen className="w-4 h-4" />
        <span>Posez-moi n'importe quelle question pour commencer</span>
      </div>

      {/* Feature cards grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 w-full max-w-4xl">
        {features.map((feature, index) => {
          const Icon = feature.icon;
          
          return (
            <div
              key={feature.title}
              className={`
                bg-card/50 backdrop-blur-sm 
                border border-border 
                rounded-xl p-6 
                ${feature.borderColor}
                transition-all duration-300 
                hover:scale-105 hover:shadow-lg
                cursor-pointer
                animate-fade-in
              `}
              style={{ animationDelay: `${index * 100}ms` }}
            >
              {/* Icon container */}
              <div className={`${feature.iconBgColor} w-12 h-12 rounded-lg flex items-center justify-center mb-4 transition-transform duration-300 group-hover:scale-110`}>
                <Icon className={`w-6 h-6 ${feature.iconColor}`} />
              </div>

              {/* Feature title */}
              <h3 className="text-foreground font-semibold mb-2">
                {feature.title}
              </h3>

              {/* Feature description */}
              <p className="text-muted-foreground text-sm leading-relaxed">
                {feature.description}
              </p>
            </div>
          );
        })}
      </div>
      {/* Bottom hint */}
      <div className="mt-12 text-center">
        <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 border border-primary/20 rounded-full">
          <Sparkles className="w-4 h-4 text-primary animate-pulse" />
          <span className="text-sm text-muted-foreground">
            💡 Astuce : Vous pouvez poser des questions en français ou en anglais
          </span>
        </div>
      </div>
    </div>
  );
};

export default WelcomeScreen;