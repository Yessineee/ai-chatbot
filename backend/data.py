intents = {
    "salutation": [
        "bonjour",
        "salut",
        "bonsoir",
        "bonjour comment ca va",
        "salut j'ai une question",
        "hello",
        "hi",
        "hey",
        "good morning",
        "good evening"
    ],
    "stage": [
        "je cherche un stage",
        "stage pfe",
        "je veux un stage de fin d'etudes",
        "comment trouver un stage",
        "je veux faire un stage",
        "est ce que vous proposez des stages",
        "je suis etudiant et je cherche un stage pfe",
        "avez vous des offres de stage",
        "stage de fin d'études",
        "comment postuler pour un stage",

        "internship",
        "i am looking for an internship",
        "internship opportunity"
    ],
    "remerciement": [
        "merci",
        "merci beaucoup",
        "thanks",
        "je vous remercie"
    ],
    "au_revoir": [
        "au revoir",
        "bye",
        "à bientôt",
        "bonne journée"
    ],
    "horaire": [
        "quels sont vos horaires",
        "horaire de travail",
        "heures d'ouverture",
        "à quelle heure vous ouvrez",
        "à quelle heure vous fermez",
        "working hours",
        "what are your working hours",
        "opening hours"
    ],
    "contact": [
        "comment vous contacter",
        "adresse email",
        "numero de telephone",
        "contact",
        "email",
        "telephone",
        "numéro",
        "comment vous contacter",
        "comment puis-je vous joindre",
        "how can i contact you",
        "contact details"
    ],
    "unknown": [
        "asdfgh",
        "je sais pas",
        "n'importe quoi",
        "aucune idée",
        "blabla"
    ],
    "etat": [
        # French
        "comment ça va",
        "comment allez-vous",
        "ça va",
        "comment vas-tu",

        # English
        "how are you",
        "how are you doing",
        "are you okay",
        "what's up"
    ],

    "identite": [
        # French
        "qui es-tu",
        "c'est quoi ton rôle",
        "que fais-tu",

        # English
        "who are you",
        "what are you",
        "what do you do"
    ],
    "recall_email": [
        # English
        "what is my email",
        "do you remember my email",
        "tell me my email",

        # French
        "quel est mon email",
        "tu te souviens de mon email",
        "c'est quoi mon email"
    ]
}
reponses = {
    "salutation": "Bonjour 👋 Je suis l’assistant virtuel de l’entreprise. Comment puis-je vous aider aujourd’hui ?",
    "stage":(
            "Nous proposons régulièrement des stages PFE et des stages d’été. "
            "Vous pouvez consulter nos offres sur notre site officiel ou nous envoyer votre CV."
    ),
    "contact": (
        "Vous pouvez nous contacter par email à contact@entreprise.com "
        "ou par téléphone au +216 XX XXX XXX."
    ),
    "remerciement": "Avec plaisir 😊 N’hésitez pas si vous avez d’autres questions.",
    "horaire": "Nos horaires sont de 9h à 17h.",
    "unknown": "Je n’ai pas bien compris votre demande 🤔. Pouvez-vous reformuler ou préciser votre question ? ",
    "etat": ["Je vais très bien 😊 Merci de demander ! Et vous ?" ,"Tout va bien de mon côté 👍 Comment puis-je vous aider ?"],
    "identite": "Je suis un assistant virtuel conçu pour répondre à vos questions." "Je suis un chatbot intelligent qui peut vous aider avec des informations générales."
}

time=["heure","time","wakt","hour","hours"]
bye=["bye", "revoir", "quitter", "ciao","au revoir","goodbye"]

import operator

# Define supported operators
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}


questions = []
labels = []

for intent, examples in intents.items():
    for ex in examples:
        questions.append(ex)
        labels.append(intent)