from flask import Flask, jsonify, request, render_template
from .email_service import send_mail
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib
import os
import json
from . import app

# Load the pre-trained machine learning model
model_path = os.path.join(os.path.dirname(__file__), 'models/clf.pkl')
model = joblib.load(model_path)

# Temporary global variable to store latest user metrics
latest_user_metrics = None

# Define the main route for the application
@app.route("/", methods=["GET", "POST"])
def index():
    """
    Handles requests to the root URL ("/") for the application.
    -GET: Serves the HTML template for the main application.
    -POST: Processes the form data from the client, runs predictions, and returns results.
    """

    if request.method == "POST":
        # Retrieve JSON data from the fetch request
        data = request.get_json()
        
        # Parse form data
        try:
            age = int(data.get("age"))
            sex = int(data.get("sex"))
            chest_pain = int(data.get("chest_pain"))
            resting_bp = int(data.get("resting_bp"))
            cholesterol = int(data.get("cholesterol"))
            fasting_bs = int(data.get("fasting_bs"))
            resting_ecg = int(data.get("resting_ecg"))
            max_hr = int(data.get("max_hr"))
            exercise_angina = int(data.get("exercise_angina"))
            oldpeak = float(data.get("oldpeak"))
            st_slope = int(data.get("st_slope"))
        except (TypeError, ValueError):
            # Handle invalid input
            return jsonify({"error": "Invalid input"}), 400

        # Create a DataFrame for prediction
        input_data = pd.DataFrame({
            'Age': [age],
            'Sex': [sex],
            'ChestPainType': [chest_pain],
            'RestingBP': [resting_bp],
            'Cholesterol': [cholesterol],
            'FastingBS': [fasting_bs],
            'RestingECG': [resting_ecg],
            'MaxHR': [max_hr],
            'ExerciseAngina': [exercise_angina],
            'Oldpeak': [oldpeak],
            'ST_Slope': [st_slope]
        })

        # Make prediction using the model
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1] * 100
        
        # Map values to text
        SEX_MAPPING = {0: "Female", 1: "Male"}
        CHEST_PAIN_MAPPING = {0: "Typical Angina", 1: "Atypical Angina", 2: "Non-Anginal Pain", 3: "Asymptomatic"}
        FASTING_BS_MAPPING = {0: "120mg/dl or under", 1: "Over 120mg/dl"}
        RESTING_ECG_MAPPING = {0: "Normal", 1: "ST", 2: "LVH"}
        EXERCISE_ANGINA_MAPPING = {0: "No", 1: "Yes"}
        ST_SLOPE_MAPPING = {0: "Up", 1: "Flat", 2: "Down"}
        
        # Create metrics JSON for LLM
        user_metrics = {
            "Age": age,
            "Sex": SEX_MAPPING.get(sex, "Unknown"),
            "Chest Pain Type": CHEST_PAIN_MAPPING.get(chest_pain, "Unknown"),
            "Resting BP": resting_bp,
            "Cholesterol": cholesterol,
            "Fasting Blood Sugar": FASTING_BS_MAPPING.get(fasting_bs, "Unknown"),
            "Resting ECG": RESTING_ECG_MAPPING.get(resting_ecg, "Unknown"),
            "Max Heart Rate": max_hr,
            "Exercise Angina": EXERCISE_ANGINA_MAPPING.get(exercise_angina, "Unknown"),
            "Oldpeak": oldpeak,
            "ST Slope": ST_SLOPE_MAPPING.get(st_slope, "Unknown"),
            "Prediction": "Positive" if prediction else "Negative",
            "Probability": f"{probability:.2f}%"
        }

        global latest_user_metrics
        latest_user_metrics = user_metrics
        
        # Send back JSON response with prediction and probability
        return jsonify({
            "prediction": int(prediction.item()), # Convert numpy type to Python for JSON serialization
            "probability": float(probability)})  # " "    

    # Render HTML template on GET request
    return render_template("index.html")

@app.route("/send-summary", methods=["POST"])
def send_summary():
    global latest_user_metrics

    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    if not latest_user_metrics:
        return jsonify({"error": "No metrics available to send"}), 400
    
    summary = json.dumps(latest_user_metrics, indent=4)

    print("Formatted Summary:\n", summary)
    return jsonify({"message": "Summary prepared successfully"})

# Test email service
@app.route("/test-email", methods=["GET"])
def test_email():
    """
    Test endpoint to verify email functionality.
    """
    try:
        # Call the send_mail function
        success = send_mail(
            to_email="email.service.54321@gmail.com",  # Replace with recipient's email address
            subject="Test Email from Flask App",
            body="This is a test email sent from the Flask app."
        )

        # Return success or failure response
        if success:
            return jsonify({"message": "Email sent successfully!"}), 200
        else:
            return jsonify({"message": "Failed to send email."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

