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

        # Send back JSON response with prediction and probability
        return jsonify({
            "prediction": int(prediction.item()), # Convert numpy type to Python for JSON serialization
            "probability": float(probability)})  # " "

    # Render HTML template on GET request
    return render_template("index.html")

