import os
import sys
import joblib
import numpy as np

# --------------------------------------------------
# Add project root to Python path
# --------------------------------------------------
current_dir = os.path.dirname(__file__)        # models/
project_root = os.path.dirname(current_dir)    # Healthcare-AI/
sys.path.append(project_root)

from preprocessing.brain_process import extract_brain_features
# --------------------------------------------------

# Load trained model and scaler
model_path = os.path.join(current_dir, "brain_model.pkl")
scaler_path = os.path.join(current_dir, "brain_scaler.pkl")

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)


def predict_brain_tumor(image_path: str) -> str:
    """
    Predict brain tumor from MRI image path
    """

    # Extract features (MUST match training)
    features = extract_brain_features(image_path)

    # Safety check
    if not isinstance(features, np.ndarray):
        raise ValueError("extract_brain_features must return a NumPy array")

    if features.shape[1] != scaler.n_features_in_:
        raise ValueError(
            f"Feature mismatch: expected {scaler.n_features_in_}, "
            f"got {features.shape[1]}"
        )

    # Scale features
    features_scaled = scaler.transform(features)

    # Predict
    prediction = model.predict(features_scaled)[0]

    return "Tumor Detected" if prediction == 1 else "No Tumor Detected"


# ---------------- TEST ----------------
if __name__ == "__main__":
    test_image = r"C:\Users\Lenovo\Healthcare-AI\Healthcare-AI\data\brain_tumor_dataset\yes\Y3.jpg"
    print(predict_brain_tumor(test_image))
