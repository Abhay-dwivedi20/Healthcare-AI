from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from chatbot.chatbot_engine import chatbot_reply
from models.brain import predict_brain_tumor

import cv2
import numpy as np
import joblib
import os

app = Flask(__name__)

# ---------- CONFIGURATION ----------
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB upload limit

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, "brain"), exist_ok=True)

# ---------- LOAD MODELS ----------
try:
    print("Loading ML models...")
    diabetes_model = joblib.load(os.path.join(MODEL_DIR, "diabetes_model.pkl"))
    diabetes_scaler = joblib.load(os.path.join(MODEL_DIR, "diabetes_scaler.pkl"))
    print("✓ Diabetes model loaded")
    
    heart_model = joblib.load(os.path.join(MODEL_DIR, "heart_model.pkl"))
    heart_scaler = joblib.load(os.path.join(MODEL_DIR, "heart_scaler.pkl"))
    print("✓ Heart model loaded")
    
    brain_model = joblib.load(os.path.join(MODEL_DIR, "brain_model.pkl"))
    brain_scaler = joblib.load(os.path.join(MODEL_DIR, "brain_scaler.pkl"))
    print("✓ Brain model loaded")
    
except Exception as e:
    print(f"✗ ERROR loading models: {e}")
    diabetes_model = heart_model = brain_model = None
    diabetes_scaler = heart_scaler = brain_scaler = None

# ---------- HELPER FUNCTIONS ----------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_diabetes_data(form_data):
    return {
        "Pregnancies": int(form_data.get("pregnancies", 0)),
        "Glucose": int(form_data.get("glucose", 0)),
        "BloodPressure": int(form_data.get("blood_pressure", 0)),
        "SkinThickness": int(form_data.get("skin_thickness", 0)),
        "Insulin": int(form_data.get("insulin", 0)),
        "BMI": float(form_data.get("bmi", 0)),
        "DiabetesPedigreeFunction": float(form_data.get("diabetes_pedigree", 0)),
        "Age": int(form_data.get("age", 0))
    }

def format_heart_data(form_data):
    return {
        "age": int(form_data.get("age", 0)),
        "sex": int(form_data.get("sex", 0)),
        "cp": int(form_data.get("cp", 0)),
        "trestbps": int(form_data.get("trestbps", 0)),
        "chol": int(form_data.get("chol", 0)),
        "fbs": int(form_data.get("fbs", 0)),
        "restecg": int(form_data.get("restecg", 0)),
        "thalach": int(form_data.get("thalach", 0)),
        "exang": int(form_data.get("exang", 0)),
        "oldpeak": float(form_data.get("oldpeak", 0)),
        "slope": int(form_data.get("slope", 0)),
        "ca": int(form_data.get("ca", 0)),
        "thal": int(form_data.get("thal", 0))
    }

# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template("index.html")

# ---------- DIABETES ----------
@app.route("/predict/diabetes", methods=["GET"])
def diabetes_form():
    return render_template("diabetes.html")

@app.route("/predict/diabetes", methods=["POST"])
def predict_diabetes():
    if diabetes_model is None:
        return render_template("error.html", error="Diabetes model not loaded")

    data = format_diabetes_data(request.form)
    features = list(data.values())
    scaled = diabetes_scaler.transform([features])
    prediction = diabetes_model.predict(scaled)[0]

    confidence = max(diabetes_model.predict_proba(scaled)[0]) if hasattr(diabetes_model, "predict_proba") else 0.85

    return render_template("result.html", disease="diabetes",
                           result={"prediction": prediction, "confidence": confidence, "input_data": data})

# ---------- HEART ----------
@app.route("/predict/heart", methods=["GET"])
def heart_form():
    return render_template("heart.html")

@app.route("/predict/heart", methods=["POST"])
def predict_heart():
    if heart_model is None:
        return render_template("error.html", error="Heart model not loaded")

    data = format_heart_data(request.form)
    features = list(data.values())
    scaled = heart_scaler.transform([features])
    prediction = heart_model.predict(scaled)[0]

    confidence = max(heart_model.predict_proba(scaled)[0]) if hasattr(heart_model, "predict_proba") else 0.88

    return render_template("result.html", disease="heart",
                           result={"prediction": prediction, "confidence": confidence, "input_data": data})

# ---------- BRAIN ----------
@app.route("/predict/brain", methods=["GET"])
def brain_form():
    return render_template("brain.html")


@app.route("/predict/brain", methods=["POST"])
def predict_brain_ui():
    if "mri_image" not in request.files:
        return render_template("error.html", error="No image uploaded")

    file = request.files["mri_image"]
    if file.filename == "":
        return render_template("error.html", error="No file selected")

    if not allowed_file(file.filename):
        return render_template("error.html", error="Invalid file type")

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, "brain", filename)
    file.save(path)

    try:
        prediction_result = predict_brain_tumor(path)

        return render_template(
            "result.html",
            disease="brain",
            result={
                "prediction": prediction_result,   # ✅ string is OK here
                "confidence": None,                # ✅ NOT a string number
                "input_data": {"filename": filename}
            }
        )

    except Exception as e:
        return render_template("error.html", error=str(e))



# ---------- CHATBOT ----------
@app.route("/chat", methods=["GET"])
def chat_page():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json if request.is_json else request.form
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "Message required"}), 400

    reply = chatbot_reply(message)
    return jsonify({"user": message, "bot": reply})

# ---------- API (BRAIN FIXED TOO) ----------
@app.route("/predict/brain", methods=["POST"])
def predict_brain():
    if "mri_image" not in request.files:
        return render_template("error.html", error="No image uploaded")

    file = request.files["mri_image"]

    if file.filename == "":
        return render_template("error.html", error="No file selected")

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, "brain", filename)
    file.save(path)

    try:
        # 🔥 THIS IS WHERE YOU USE IT
        prediction_result = predict_brain_tumor(path)

        return render_template(
            "result.html",
            disease="brain",
            result={
                "prediction": prediction_result,
                "confidence": "Model-based",
                "input_data": {"filename": filename}
            }
        )

    except Exception as e:
        return render_template("error.html", error=str(e))


# ---------- HEALTH ----------
@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

# ---------- MAIN ----------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
