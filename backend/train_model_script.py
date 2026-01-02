

import sys
from pathlib import Path
import logging
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from model import train_model, save_model, preprocess, MODEL_PATH
    from data import questions, labels
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error("Make sure model.py and data.py are in the same directory")
    sys.exit(1)


def evaluate_model(vectorizer, model, X, y):
    
    logger.info("Evaluating model...")

    # Transform test data
    X_processed = [preprocess(x) for x in X]
    X_vec = vectorizer.transform(X_processed)

    # Predict
    y_pred = model.predict(X_vec)

    # Calculate metrics
    accuracy = accuracy_score(y, y_pred)

    logger.info(f"Accuracy: {accuracy:.2%}")
    logger.info("\nClassification Report:")
    print(classification_report(y, y_pred))

    return {
        "accuracy": float(accuracy),
        "total_samples": len(y)
    }


def main():
    """Main training function"""
    logger.info("=" * 60)
    logger.info("CHATBOT MODEL TRAINING")
    logger.info("=" * 60)

    # Check if data is available
    if not questions or not labels:
        logger.error("No training data found!")
        logger.error("Make sure data.py contains 'questions' and 'labels'")
        return False

    logger.info(f"Training data: {len(questions)} samples")
    logger.info(f"Unique labels: {len(set(labels))}")

    # Split data for evaluation (80/20)
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            questions,
            labels,
            test_size=0.2,
            random_state=42,
            stratify=labels
        )
        logger.info(f"Train set: {len(X_train)} samples")
        logger.info(f"Test set: {len(X_test)} samples")
    except Exception as e:
        logger.warning(f"Could not split data: {e}")
        logger.warning("Training on full dataset without evaluation")
        X_train, X_test = questions, []
        y_train, y_test = labels, []

    # Train model
    try:
        logger.info("\nTraining model...")

        # Create custom training data structure
        intents_data = {
            'intents': []  # Add your actual intents structure if needed
        }

        vectorizer, model = train_model(intents_data)
        logger.info("✓ Model trained successfully!")

    except Exception as e:
        logger.error(f"✗ Error training model: {e}")
        return False

    # Evaluate if we have test data
    metrics = {}
    if X_test and y_test:
        try:
            metrics = evaluate_model(vectorizer, model, X_test, y_test)
        except Exception as e:
            logger.warning(f"Could not evaluate model: {e}")

    # Save model
    try:
        logger.info(f"\nSaving model to {MODEL_PATH}...")
        save_model(vectorizer, model)
        logger.info("✓ Model saved successfully!")

        # Save metrics
        if metrics:
            metrics_path = MODEL_PATH.parent / "metrics.json"
            with open(metrics_path, 'w') as f:
                json.dump(metrics, f, indent=2)
            logger.info(f"✓ Metrics saved to {metrics_path}")

    except Exception as e:
        logger.error(f"✗ Error saving model: {e}")
        return False

    logger.info("\n" + "=" * 60)
    logger.info("TRAINING COMPLETED SUCCESSFULLY!")
    logger.info("=" * 60)
    logger.info(f"Model saved to: {MODEL_PATH}")
    logger.info("You can now use this model in your chatbot")

    return True


if __name__ == "__main__":
    success = main()

    sys.exit(0 if success else 1)
