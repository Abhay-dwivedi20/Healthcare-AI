import os
import sys
import joblib

from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# --------------------------------------------------
# Add project root to Python path
# --------------------------------------------------
current_dir = os.path.dirname(__file__)        # models/
project_root = os.path.dirname(current_dir)    # Healthcare-AI/
sys.path.append(project_root)

from preprocessing.heart_process import prepare_heart_data
# --------------------------------------------------


def train_heart_model():
    """
    Train Gaussian Naive Bayes model for Heart Disease prediction
    """

    data_path = os.path.join(project_root, "data", "heart.csv")

    # Load and preprocess data
    X, y, scaler = prepare_heart_data(data_path)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Final selected model (from notebook)
    model = GaussianNB()
    model.fit(X_train, y_train)

    # Evaluation
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"\nHeart Disease Model Accuracy: {acc * 100:.2f}%\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Save model & scaler
    model_path = os.path.join(current_dir, "heart_model.pkl")
    scaler_path = os.path.join(current_dir, "heart_scaler.pkl")

    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)

    print("\nTraining complete. Artifacts saved in models folder.")
    print("Model path:", model_path)
    print("Scaler path:", scaler_path)


if __name__ == "__main__":
    train_heart_model()
