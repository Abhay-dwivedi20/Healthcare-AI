# 🏥 Healthcare AI – Multi-Disease Prediction Web Application
## 📌 Project Overview

Healthcare AI is a modular web-based application built using Python, Machine Learning, Flask, and SQLite, designed to assist non-technical users in predicting multiple diseases using simple inputs such as medical parameters or MRI images.

    .  The system currently supports:
    .  Diabetes Prediction
    .  Heart Disease Prediction
    .  Brain Tumor Detection (MRI Image)      
    .  Medical Chatbot      
    .  Prediction History Tracking

This project follows a clean, scalable architecture with clear separation between the UI layer, backend logic, ML models, chatbot, and database, making it suitable for academic evaluation and future expansion.

## 🎯 Key Features
## 🩸 Diabetes Prediction

    Input: Health parameters via form
    
    Model: Random Forest
    
    Output: Prediction with confidence score

## ❤️ Heart Disease Prediction

    Input: Clinical parameters
    
    Model: Gaussian Naive Bayes
    
    Output: Risk assessment with confidence

## 🧠 Brain Tumor Detection

    Input: MRI image upload
    
    Image preprocessing using OpenCV
    
    Output: Tumor detected / not detected

## 💬 Medical Chatbot

    Rule-based responses for common medical queries
    
    Stores chat history in database
    
    Designed for general medical guidance (educational use)

## 📊 Prediction History

    View all past predictions
    
    Data fetched from relational database
    
    Improves transparency and usability

## 🧠 Technology Stack

    Backend
    Python 3.10
    Flask
    SQLite
    Machine Learning
    NumPy
    Pandas
    Scikit-learn
    OpenCV
    Frontend
    HTML
    Bootstrap
    Jinja2 Templates
    Tools
    VS Code
    Git & GitHub
    Virtual Environment

## 🗂️ Project Structure

    Healthcare-AI/
    │
    ├── app.py                      # Main Flask application
    │
    ├── models/                     # Trained ML models
    │   ├── diabetes_model.pkl
    │   ├── diabetes_scaler.pkl
    │   ├── heart_model.pkl
    │   ├── heart_scaler.pkl
    │   ├── brain_model.pkl
    │   └── brain_scaler.pkl
    │
    ├── preprocessing/              # Data & image preprocessing
    │   ├── diabetes_process.py
    │   ├── heart_process.py
    │   └── brain_process.py
    │
    ├── chatbot/                    # Chatbot logic
    │   ├── intents.py
    │   ├── responses.py
    │   └── chatbot_engine.py
    │
    ├── database/                   # Database layer
    │   ├── db.py
    │   ├── init_db.py
    │   └── operations.py
    │
    ├── templates/                  # HTML templates
    │   ├── base.html
    │   ├── index.html
    │   ├── diabetes.html
    │   ├── heart.html
    │   ├── brain.html
    │   ├── chat.html
    │   ├── history.html
    │   ├── result.html
    │   └── error.html
    │
    ├── static/                     # CSS / JS / Images
    │
    ├── uploads/                    # Runtime uploads (ignored in Git)
    │
    ├── venv/                       # Virtual environment (ignored)
    │
    ├── .gitignore
    └── README.md

## 🧩 Database Design

Tables Used:

reports – Stores disease type, input data, timestamp
diagnostic_results – Stores prediction, confidence, model used
chat_logs – Stores chatbot conversations
The database uses normalized relational design to separate input data from model outputs.

## ⚙️ How to Run the Project

**1️⃣ Clone the Repository**

    git clone <repository-url>
    cd Healthcare-AI

**2️⃣ Create Virtual Environment**

    python -m venv venv

**3️⃣ Activate Virtual Environment**

Windows

    venv\Scripts\activate

**4️⃣ Install Dependencies**

    pip install -r requirements.txt

**5️⃣ Initialize Database**

    python database/init_db.py

**6️⃣ Run the Application**

    python app.py

**7️⃣ Open in Browser**

    http://localhost:5000

## 🔐 Important Notes

healthcare.db is not committed to GitHub (runtime data)
uploads/ folder is ignored to protect user images
This project is for educational purposes only
AI predictions do not replace professional medical advice

## 🚀 Future Enhancements

Chest Scan (X-ray / CT) prediction module
User authentication
Admin dashboard
Cloud deployment
Advanced LLM-based medical chatbot

## 🎓 Academic Disclaimer

This project is developed strictly for educational and learning purposes.
All medical predictions should be validated by certified healthcare professionals.

## 👨‍💻 Author

**Abhay Dwivedi**

BCA Student

Data Science & Machine Learning Enthusiast

