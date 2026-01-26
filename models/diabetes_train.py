import os
import sys
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Add project root to path so 'preprocessing' can be found

current_dir = os.path.dirname(__file__)            # models/
project_root = os.path.dirname(current_dir)        # Healthcare-AI/
sys.path.append(project_root)

from preprocessing.diabetes_process import prepare_diabetes_data

def train_diabetes_model():
    
    # Use path relative to project root

    data_path = os.path.join(project_root, "data", "diabetes.csv")
    X, y, scaler = prepare_diabetes_data(data_path)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)

    # Save artifacts in the models/ folder
    
    joblib.dump(model, os.path.join(current_dir, "diabetes_model.pkl"))
    joblib.dump(scaler, os.path.join(current_dir, "diabetes_scaler.pkl"))
    print("Training complete. Artifacts saved in models/ folder.")

if __name__ == "__main__":
    train_diabetes_model()