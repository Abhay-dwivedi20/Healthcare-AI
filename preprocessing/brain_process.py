import cv2
import numpy as np


def extract_brain_features(image_path):
    """
    Extract features from a brain MRI image
    """

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (128, 128))

    mean = np.mean(img)
    std = np.std(img)

    return np.array([[mean, std]])  # shape (1, 2)
