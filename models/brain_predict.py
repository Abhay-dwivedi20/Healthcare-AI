import os
import sys
import joblib

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


def predict_brain_tumor(image_path):
    """
    Predict brain tumor from MRI image
    """

    features = extract_brain_features(image_path)
    features_scaled = scaler.transform(features)

    prediction = model.predict(features_scaled)[0]

    return "Tumor Detected" if prediction == 1 else "No Tumor Detected"


# Test run
if __name__ == "__main__":
    test_image = r"C:\Users\Lenovo\Healthcare-AI\Healthcare-AI\data\brain_tumor_dataset\yes\Y3.jpg"  # replace with real image path
    print(predict_brain_tumor(test_image))
