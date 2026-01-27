from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Healthcare AI App is running"

if __name__ == "__main__":
    app.run(debug=True)



from flask import Flask, request, jsonify
import joblib
import os

app = Flask(__name__)

# ---------- PATH SETUP ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(BASE_DIR, "models")

# ---------- LOAD MODELS ----------
diabetes_model = joblib.load(os.path.join(MODEL_DIR, "diabetes_model.pkl"))
diabetes_scaler = joblib.load(os.path.join(MODEL_DIR, "diabetes_scaler.pkl"))

@app.route("/")
def home():
    return "Healthcare AI App is running"

@app.route("/predict/diabetes", methods=["POST"])
def predict_diabetes():
    data = request.json  # expecting JSON input

    # Convert input into model format
    features = [
        data["Pregnancies"],
        data["Glucose"],
        data["BloodPressure"],
        data["SkinThickness"],
        data["Insulin"],
        data["BMI"],
        data["DiabetesPedigreeFunction"],
        data["Age"]
    ]

    # Scale and predict
    scaled_features = diabetes_scaler.transform([features])
    prediction = diabetes_model.predict(scaled_features)[0]

    result = "Diabetes Detected" if prediction == 1 else "No Diabetes"

    return jsonify({
        "prediction": result
    })

# ---------- LOAD HEART MODEL ----------
heart_model = joblib.load(os.path.join(MODEL_DIR, "heart_model.pkl"))
heart_scaler = joblib.load(os.path.join(MODEL_DIR, "heart_scaler.pkl"))

@app.route("/predict/heart", methods=["POST"])
def predict_heart():
    data = request.json

    features = [
        data["age"],
        data["sex"],
        data["cp"],
        data["trestbps"],
        data["chol"],
        data["fbs"],
        data["restecg"],
        data["thalach"],
        data["exang"],
        data["oldpeak"],
        data["slope"],
        data["ca"],
        data["thal"]
    ]

    scaled_features = heart_scaler.transform([features])
    prediction = heart_model.predict(scaled_features)[0]

    result = "Heart Disease Detected" if prediction == 1 else "No Heart Disease"

    return jsonify({
        "prediction": result
    })





if __name__ == "__main__":
    app.run(debug=False)
