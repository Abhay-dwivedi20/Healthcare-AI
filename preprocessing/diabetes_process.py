import pandas as pd
from sklearn.preprocessing import StandardScaler

filepath = "data/diabetes.csv"

def prepare_diabetes_data(filepath):

    """Loads, cleans, and scales the diabetes dataset."""
    
    df = pd.read_csv(filepath)
    
    # Example cleaning: Handle zero values in specific columns
    
    cols_to_fix = ['Glucose', 'BloodPressure', 'BMI']
    for col in cols_to_fix:
        df[col] = df[col].replace(0, df[col].median())

    X = df.drop('Outcome', axis=1)
    y = df['Outcome']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y, scaler