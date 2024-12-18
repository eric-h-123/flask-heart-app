from flask import Flask, jsonify, request, render_template
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib
import os
from . import app

# Load the pre-trained machine learning model
model_path = os.path.join(os.path.dirname(__file__), 'models/clf.pkl')
model = joblib.load(model_path)

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

        SEX_MAPPING = {0: "Female", 1: "Male"}
        CHEST_PAIN_MAPPING = {0: "Typical Angina", 1: "Atypical Angina", 2: "Non-Anginal Pain", 3: "Asymptomatic"}
        FASTING_BS_MAPPING = {0: "120mg/dl or under", 1: "Over 120mg/dl"}
        RESTING_ECG_MAPPING = {0: "Normal", 1: "ST", 2: "LVH"}
        EXERCISE_ANGINA_MAPPING = {0: "No", 1: "Yes"}
        ST_SLOPE_MAPPING = {0: "Up", 1: "Flat", 2: "Down"}

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
        import json
        print(json.dumps(user_metrics, indent=4))

        # Send back JSON response with prediction and probability
        return jsonify({
            "prediction": int(prediction.item()), # Convert numpy type to Python for JSON serialization
            "probability": float(probability)})  # " "    

    # Render HTML template on GET request
    return render_template("index.html")
    

