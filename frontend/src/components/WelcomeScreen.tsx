import { MessageSquare, Sparkles, Brain, Zap } from "lucide-react";

const WelcomeScreen = () => {
  return (
    <div className="flex flex-col items-center justify-center py-12 animate-fade-in">
      {/* Main Icon with glow effect */}
      <div className="relative mb-8">
        <div className="absolute inset-0 bg-teal-500/20 rounded-full blur-2xl animate-pulse"></div>
        <div className="relative bg-teal-500/10 p-8 rounded-full border border-teal-500/20">
          <MessageSquare className="w-16 h-16 text-teal-500" />
        </div>
      </div>

      {/* Welcome text */}
      <h2 className="text-3xl font-bold text-white mb-3">
        Assistant IA <span className="text-teal-500">✨</span>
      </h2>
      <p className="text-gray-400 text-center max-w-md mb-12">
        Votre compagnon intelligent pour répondre à vos questions, vous aider dans vos tâches et explorer de nouvelles idées.
      </p>

      {/* Feature cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-2xl">
        <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-lg p-6 hover:border-teal-500/30 transition-all duration-300 hover:scale-105">
          <div className="bg-teal-500/10 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
            <Brain className="w-6 h-6 text-teal-500" />
          </div>
          <h3 className="text-white font-semibold mb-2">Intelligence Avancée</h3>
          <p className="text-gray-400 text-sm">
            Réponses précises et contextuelles à vos questions
          </p>
        </div>

        <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-lg p-6 hover:border-teal-500/30 transition-all duration-300 hover:scale-105">
          <div className="bg-cyan-500/10 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
            <Sparkles className="w-6 h-6 text-cyan-500" />
          </div>
          <h3 className="text-white font-semibold mb-2">Créativité</h3>
          <p className="text-gray-400 text-sm">
            Génération de contenu créatif et original
          </p>
        </div>

        <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-lg p-6 hover:border-teal-500/30 transition-all duration-300 hover:scale-105">
          <div className="bg-purple-500/10 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
            <Zap className="w-6 h-6 text-purple-500" />
          </div>
          <h3 className="text-white font-semibold mb-2">Rapidité</h3>
          <p className="text-gray-400 text-sm">
            Réponses instantanées pour une productivité maximale
          </p>
        </div>
      </div>
    </div>
  );
};

export default WelcomeScreen;