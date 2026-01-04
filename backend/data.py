import json
import os
import operator
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define supported operators
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

# Load intents from JSON file
intents_file = os.path.join(os.path.dirname(__file__), 'intents.json')

try:
    with open(intents_file, 'r', encoding='utf-8') as f:
        intents_data = json.load(f)
    logger.info(f"✓ Successfully loaded intents from {intents_file}")
except FileNotFoundError:
    logger.error(f"Error: {intents_file} not found. Using minimal default data.")
    intents_data = {
        "intents": [
            {
                "tag": "greeting",
                "patterns": ["hello", "hi", "hey"],
                "responses": ["Hello!", "Hi there!"]
            }
        ]
    }
except json.JSONDecodeError as e:
    logger.error(f"Error: Invalid JSON in {intents_file}: {e}")
    intents_data = {"intents": []}

# Initialize data structures
questions = []
labels = []
reponses = {}

# Process intents
loaded_intents = []
missing_responses = []

for intent in intents_data.get('intents', []):
    tag = intent.get('tag')
    patterns = intent.get('patterns', [])
    responses = intent.get('responses', [])

    if not tag:
        logger.warning(f"Skipping intent without tag: {intent}")
        continue

    loaded_intents.append(tag)

    # Add patterns to training data
    if patterns:
        for pattern in patterns:
            questions.append(pattern)
            labels.append(tag)
    else:
        logger.warning(f"⚠ Intent '{tag}' has no patterns!")

    # Add responses
    if responses:
        reponses[tag] = responses
    else:
        logger.warning(f"⚠ Intent '{tag}' has NO responses!")
        missing_responses.append(tag)
        # Add default response to prevent crashes
        reponses[tag] = [f"Je peux vous aider avec {tag}."]

# Ensure 'unknown' intent exists
if 'unknown' not in reponses:
    reponses['unknown'] = [
        "Je n'ai pas bien compris votre demande 🤔. Pouvez-vous reformuler ou préciser votre question ?",
        "I'm not sure I understand. Could you rephrase that?",
        "I didn't quite get that. Can you try asking differently?",
        "Hmm, I'm not sure about that. Can you be more specific?"
    ]

# Ensure 'etat' intent exists (for "how are you")
if 'etat' not in reponses:
    reponses['etat'] = [
        "Je vais très bien 😊 Merci de demander ! Et vous ?",
        "Tout va bien de mon côté 👍 Comment puis-je vous aider ?",
        "I'm doing well, thank you! How can I help you?",
        "Great, thanks for asking! What can I do for you?",
        "Je vais bien, merci! Comment puis-je vous aider?"
    ]

# Additional helper lists
time = ["heure", "time", "wakt", "hour", "hours", "temps"]
bye = ["bye", "revoir", "quitter", "ciao", "au revoir", "see you", "goodbye"]

# Statistics and validation
logger.info("=" * 60)
logger.info("DATA LOADING SUMMARY")
logger.info("=" * 60)
logger.info(f"✓ Loaded {len(questions)} training examples")
logger.info(f"✓ Number of unique intents: {len(set(labels))}")
logger.info(f"✓ Intents with responses: {len(reponses)}")

logger.info(f"\n📋 All loaded intents:")
for intent in sorted(loaded_intents):
    pattern_count = labels.count(intent)
    response_count = len(reponses.get(intent, []))
    logger.info(f"  • {intent}: {pattern_count} patterns, {response_count} responses")

if missing_responses:
    logger.warning(f"\n⚠ WARNING: These intents have NO responses in intents.json:")
    for tag in missing_responses:
        logger.warning(f"  • {tag}")
    logger.warning("Default responses were added to prevent crashes.")

# Check for common intents that should exist
required_intents = ['greeting', 'goodbye', 'thanks', 'unknown']
missing_required = [intent for intent in required_intents if intent not in loaded_intents]
if missing_required:
    logger.warning(f"\n⚠ Missing recommended intents: {', '.join(missing_required)}")

logger.info("=" * 60)

# For debugging - run this file directly to see what was loaded
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("DETAILED DATA INSPECTION")
    print("=" * 60)

    # Show sample training data
    print("\n📝 First 10 training samples:")
    for i in range(min(10, len(questions))):
        print(f"  {i + 1}. Pattern: '{questions[i][:50]}' → Label: '{labels[i]}'")

    # Show all responses
    print("\n💬 Sample responses for each intent:")
    for tag in sorted(reponses.keys()):
        print(f"\n  {tag.upper()}:")
        for resp in reponses[tag][:2]:  # Show first 2 responses
            print(f"    - {resp[:70]}...")

    # Show statistics
    print("\n📊 Intent distribution:")
    from collections import Counter

    intent_counts = Counter(labels)
    for intent, count in intent_counts.most_common():
        print(f"  {intent}: {count} patterns")

    print("\n✓ Data loading completed successfully!")
    print("=" * 60)
