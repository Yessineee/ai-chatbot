import { Lightbulb, Code, BookOpen, Palette } from "lucide-react";

interface SuggestedPromptsProps {
  onPromptClick: (prompt: string) => void;
}

const prompts = [
  {
    icon: Lightbulb,
    text: "Explique-moi un concept complexe",
    color: "text-yellow-500",
    bgColor: "bg-yellow-500/10",
    borderColor: "border-yellow-500/20",
    hoverBorder: "hover:border-yellow-500/50"
  },
  {
    icon: Code,
    text: "Aide-moi à résoudre un problème de code",
    color: "text-blue-500",
    bgColor: "bg-blue-500/10",
    borderColor: "border-blue-500/20",
    hoverBorder: "hover:border-blue-500/50"
  },
  {
    icon: BookOpen,
    text: "Résume un article ou un document",
    color: "text-green-500",
    bgColor: "bg-green-500/10",
    borderColor: "border-green-500/20",
    hoverBorder: "hover:border-green-500/50"
  },
  {
    icon: Palette,
    text: "Crée quelque chose de créatif",
    color: "text-purple-500",
    bgColor: "bg-purple-500/10",
    borderColor: "border-purple-500/20",
    hoverBorder: "hover:border-purple-500/50"
  },
];

const SuggestedPrompts = ({ onPromptClick }: SuggestedPromptsProps) => {
  return (
    <div className="py-4 animate-fade-in">
      <p className="text-gray-400 text-sm mb-3 text-center">
        💡 Suggestions pour continuer
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {prompts.map((prompt, index) => {
          const Icon = prompt.icon;
          return (
            <button
              key={index}
              onClick={() => onPromptClick(prompt.text)}
              className={`flex items-center gap-3 p-4 rounded-lg border ${prompt.borderColor} ${prompt.bgColor} ${prompt.hoverBorder} hover:scale-[1.02] transition-all duration-200 text-left group`}
            >
              <div className={`${prompt.bgColor} p-2 rounded-lg`}>
                <Icon className={`w-5 h-5 ${prompt.color}`} />
              </div>
              <span className="text-gray-300 text-sm group-hover:text-white transition-colors">
                {prompt.text}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default SuggestedPrompts;