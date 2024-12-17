
# **Heart Disease Prediction Web Application**

## **Overview**
This is a web application designed to predict the likelihood of heart disease based on user-provided health metrics. The application uses machine learning and provides predictions along with confidence probabilities. It is securely hosted and accessible online.

**Live Application**: [Heart Disease Predictor](https://www.ericheinrich.dev)

---

## **Features**
- **Heart Disease Prediction**: Uses a trained machine learning model to predict the likelihood of heart disease.
- **Confidence Score**: Provides a confidence probability for each prediction.
- **Pre-filled Data**: "Load Sample Data" feature allows users to test the app without entering manual data.
- **Secure Hosting**: Hosted on an AWS EC2 instance with SSL encryption for secure communication.
- **Responsive Design**: Works across desktop and mobile devices for seamless user experience.

---

## **Setup Instructions**

### **Prerequisites**
To run the project locally, ensure you have:
- **Python 3.8+**
- **pip** (Python package manager)
- **Git**

---

### **Download the Project**
Clone the repository:
```bash
git clone https://github.com/yourusername/heart-disease-predictor.git
cd heart-disease-predictor
```

---

### **Set Up Virtual Environment**
On Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:
```cmd
python -m venv venv
venv\Scripts\activate
```

---

### **Install Dependencies**
Install the required Python packages:
```bash
pip install -r requirements.txt
```

---

### **Run the Application**
Set the environment variable and start the server:

**Linux/Mac:**
```bash
export FLASK_APP=webapp
export FLASK_ENV=development
flask run
```

**Windows (PowerShell):**
```powershell
$env:FLASK_APP = "webapp"
$env:FLASK_ENV = "development"
flask run
```

The application will be accessible at:
```
http://127.0.0.1:5000
```

---

## **Usage**
1. **Access the Application**:
   - Visit the live app: [Heart Disease Predictor](https://www.ericheinrich.dev)
   - Or run locally as described above.

2. **Enter Health Metrics**:
   - Fill in the form with your health data (e.g., age, cholesterol level, etc.).
   - Alternatively, click **"Load Sample Data"** to auto-populate the form.

3. **View Results**:
   - Submit the form to see the prediction and confidence score.

---

## **Technologies Used**
- **Python**: Backend server logic and ML model handling.
- **Flask**: Lightweight web framework for backend.
- **Jupyter Notebooks**: Used for data exploration, cleaning, and model training.
- **Miniconda**: Environment management for running Jupyter and required libraries.
- **Scikit-learn**: Machine learning library for model creation.
- **Joblib**: For model serialization and deployment.
- **HTML/CSS (Bootstrap)**: Frontend design and responsiveness.
- **AWS EC2**: Hosting the application with SSL encryption.
- **Gunicorn**: WSGI HTTP server for running the Flask app in production.
- **Nginx**: Reverse proxy and load balancer for serving the application.
- **Let's Encrypt**: SSL certificate management for secure HTTPS communication.

---

## **Deployment Notes**
- The application is hosted on an **AWS EC2** instance.
- **Gunicorn** is used as the WSGI server to run the Flask application.
- **Nginx** serves as a reverse proxy to handle incoming requests and SSL termination.
- SSL encryption is provided by **Let's Encrypt** for secure HTTPS communication.

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## **Acknowledgments**
Special thanks to the open-source tools and libraries that made this project possible:
- Flask, Scikit-learn, and AWS services.
- **Kaggle Dataset**: Heart disease dataset used for training the model.  
  Dataset Link: [Heart Disease Dataset on Kaggle](https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction)

