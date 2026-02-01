import cv2
import numpy as np

def extract_brain_features(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Image cannot be read")

    img = cv2.resize(img, (128, 128))

    mean_intensity = float(np.mean(img))
    std_intensity = float(np.std(img))

    features = np.array([[mean_intensity, std_intensity]], dtype=np.float32)
    return features
