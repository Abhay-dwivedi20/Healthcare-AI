import pandas as pd
from sklearn.preprocessing import StandardScaler


def prepare_heart_data(filepath):
    """
    Loads, cleans, and scales the heart disease dataset
    """

    df = pd.read_csv(filepath)

    # Drop duplicates if any
    df = df.drop_duplicates()

    # Target column (common in heart datasets)
    target_col = "target" if "target" in df.columns else "Target"

    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Feature scaling (important for GaussianNB)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler


# Test run (only for verification)
if __name__ == "__main__":
    X, y, scaler = prepare_heart_data("../data/heart.csv")
    print("Heart preprocessing successful")
    print("X shape:", X.shape)
    print("y shape:", y.shape)
