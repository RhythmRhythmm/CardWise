# app.py
from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS # To handle Cross-Origin Resource Sharing

app = Flask(__name__)
CORS(app) # Enable CORS for all origins, adjust in production for specific origins

# --- 1. Load the Trained ML Model ---
# Ensure 'credit_approval_model.joblib' is in the same directory as app.py
try:
    model = joblib.load('credit_approval_model.joblib')
    print("Machine learning model loaded successfully.")
except FileNotFoundError:
    print("Error: 'credit_approval_model.joblib' not found. Please run ml_model_training.py first to train and save the model.")
    model = None # Set model to None to handle gracefully
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# --- 2. Define the expected feature columns for the model ---
# THESE MUST EXACTLY MATCH THE 'X.columns.tolist()' OUTPUT FROM ml_model_training.py
expected_features = [
    'Age', 'Income', 'Credit_Score', 'Employment_Years',
    'Debt_to_Income_Ratio', 'Loan_History_Count', 'Monthly_Rent_Mortgage',
    'Number_of_Dependents', 'Has_Student_Loan', 'Has_Auto_Loan', 'Has_Mortgage',
    'Employment_Status_Employed', 'Employment_Status_Self_Employed',
    'Employment_Status_Unemployed', 'Housing_Status_Rent', 'Housing_Status_Own'
]

# --- 3. Preprocessing Function (Crucial for consistency with training) ---
def preprocess_input(data):
    """
    Preprocesses raw input data from the frontend into a DataFrame
    suitable for the ML model.
    Ensures consistency with ml_model_training.py's feature generation.
    """
    # Initialize all expected features with default values (0 for binary/categorical, etc.)
    processed_data_dict = {
        'Age': 0, 'Income': 0, 'Credit_Score': 0, 'Employment_Years': 0,
        'Debt_to_Income_Ratio': 0.0, 'Loan_History_Count': 0, 'Monthly_Rent_Mortgage': 0,
        'Number_of_Dependents': 0, 'Has_Student_Loan': 0, 'Has_Auto_Loan': 0, 'Has_Mortgage': 0,
        'Employment_Status_Employed': 0, 'Employment_Status_Self_Employed': 0,
        'Employment_Status_Unemployed': 0, 'Housing_Status_Rent': 0, 'Housing_Status_Own': 0
    }

    # Map frontend inputs to the specific keys expected by the model
    # Numerical features
    processed_data_dict['Age'] = data.get('age', 0)
    processed_data_dict['Income'] = data.get('income', 0)
    processed_data_dict['Credit_Score'] = data.get('creditScore', 0)
    processed_data_dict['Employment_Years'] = data.get('employmentYears', 0)
    processed_data_dict['Loan_History_Count'] = data.get('loanHistoryCount', 0)
    processed_data_dict['Monthly_Rent_Mortgage'] = data.get('monthlyHousingCost', 0)
    processed_data_dict['Number_of_Dependents'] = data.get('dependents', 0)

    # Boolean/Checkbox features
    processed_data_dict['Has_Student_Loan'] = 1 if data.get('hasStudentLoan') else 0
    processed_data_dict['Has_Auto_Loan'] = 1 if data.get('hasAutoLoan') else 0
    # Has_Mortgage will be set based on either checkbox OR housing status for consistency
    processed_data_dict['Has_Mortgage'] = 1 if data.get('hasMortgage') else 0 # Start with checkbox value

    # One-hot encoded Employment Status
    emp_status = data.get('employmentStatus')
    if emp_status == 'employed':
        processed_data_dict['Employment_Status_Employed'] = 1
    elif emp_status == 'selfEmployed':
        processed_data_dict['Employment_Status_Self_Employed'] = 1
    elif emp_status == 'unemployed':
        processed_data_dict['Employment_Status_Unemployed'] = 1
    # For 'retired' or 'student', the above OHE columns remain 0, which aligns with training.

    # One-hot encoded Housing Status
    housing_status = data.get('housingStatus')
    if housing_status == 'rent':
        processed_data_dict['Housing_Status_Rent'] = 1
    elif housing_status == 'own':
        processed_data_dict['Housing_Status_Own'] = 1
    elif housing_status == 'mortgage':
        processed_data_dict['Housing_Status_Own'] = 1 # As per training data, mortgage implies owning
        processed_data_dict['Has_Mortgage'] = 1       # Also set Has_Mortgage to 1 if housing status is mortgage

    # Calculate Debt_to_Income_Ratio (DTI)
    total_monthly_outgo = processed_data_dict['Monthly_Rent_Mortgage'] + data.get('monthlyDebt', 0)
    monthly_income = (processed_data_dict['Income'] / 12) if processed_data_dict['Income'] > 0 else 0
    # Set DTI to a high value (0.65, max from training data) if income is zero to ensure consistent behavior
    processed_data_dict['Debt_to_Income_Ratio'] = (total_monthly_outgo / monthly_income) if monthly_income > 0 else 0.65

    # Create a DataFrame with a single row, ensuring all expected features are present
    # and in the correct order as defined by expected_features.
    df_input = pd.DataFrame([processed_data_dict], columns=expected_features)

    # --- Debugging: Print the DataFrame being sent to the model ---
    print("\n--- DataFrame sent to ML Model for Prediction ---")
    print(df_input)
    print("---------------------------------------------------\n")

    return df_input

# --- 4. Prediction Endpoint ---
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"approved": False, "reason": "ML model not loaded on server. Please check server logs."}), 500

    try:
        raw_data = request.get_json(force=True) # Get JSON data from request
        if not raw_data:
            return jsonify({"approved": False, "reason": "No input data provided."}), 400

        # Preprocess the input data
        input_df = preprocess_input(raw_data)

        # Make prediction
        prediction = model.predict(input_df)[0] # [0] to get the single prediction value
        prediction_proba = model.predict_proba(input_df)[0].tolist() # Probability of each class

        approved = bool(prediction) # Convert 1/0 to True/False

        reason = ""
        if approved:
            reason = "Your application aligns well with our credit criteria. We recommend proceeding with the application process."
        else:
            reason = "Your application did not meet the current eligibility criteria. Factors such as income, credit score, or existing debt may need improvement."

        return jsonify({
            "approved": approved,
            "reason": reason,
            "prediction_probability": {"rejected": prediction_proba[0], "approved": prediction_proba[1]}
        })

    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({"approved": False, "reason": f"An internal server error occurred during prediction: {str(e)}"}), 500

# --- 5. Run the Flask App ---
if __name__ == '__main__':
    # To run: python app.py
    # This will typically run on http://127.0.0.1:5000/
    # For production, use a production-ready WSGI server like Gunicorn.
    app.run(debug=True) # debug=True for development, turn off for production
