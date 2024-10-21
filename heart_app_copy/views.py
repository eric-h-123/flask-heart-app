from flask import Flask
from flask import render_template, request
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib
import os
from . import app

model_path = os.path.join(os.path.dirname(__file__), 'models/clf.pkl')
model = joblib.load(model_path)

@app.route("/", methods=["GET", "POST"])
def demo1():
    if request.method == "POST":
        # Get form data
        age = int(request.form.get("age"))
        sex = int(request.form.get("sex"))
        chest_pain = int(request.form.get("chest_pain"))
        resting_bp = int(request.form.get("resting_bp"))
        cholesterol = int(request.form.get("cholesterol"))
        fasting_bs = int(request.form.get("fasting_bs"))
        resting_ecg = int(request.form.get("resting_ecg"))
        max_hr = int(request.form.get("max_hr"))
        exercise_angina = int(request.form.get("exercise_angina"))
        oldpeak = float(request.form.get("oldpeak"))
        st_slope = int(request.form.get("st_slope"))

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

        # Render result in HTML template
        return render_template("demo1.html", result=prediction, probability=probability)

    return render_template("demo1.html")

# New functions
@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")



@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )
@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")