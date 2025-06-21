# ml_model_training.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib # For saving the model

# --- 1. Generate Synthetic Data ---
# This data mimics a real-world credit card application dataset.
# In a real scenario, you would load your actual dataset here.

np.random.seed(42) # for reproducibility

num_samples = 2000

data = {
    'Age': np.random.randint(18, 70, num_samples),
    'Income': np.random.randint(20000, 200000, num_samples),
    'Credit_Score': np.random.randint(300, 850, num_samples), # FICO score range
    'Employment_Years': np.random.randint(0, 30, num_samples),
    'Debt_to_Income_Ratio': np.random.uniform(0.05, 0.6, num_samples),
    'Loan_History_Count': np.random.randint(0, 10, num_samples),
    'Monthly_Rent_Mortgage': np.random.randint(0, 3000, num_samples), # 0 if owns home
    'Number_of_Dependents': np.random.randint(0, 5, num_samples),
    'Has_Student_Loan': np.random.choice([0, 1], num_samples, p=[0.7, 0.3]),
    'Has_Auto_Loan': np.random.choice([0, 1], num_samples, p=[0.6, 0.4]),
    'Has_Mortgage': np.random.choice([0, 1], num_samples, p=[0.5, 0.5]),
    'Employment_Status_Employed': np.random.choice([0, 1], num_samples, p=[0.1, 0.9]), # Mostly employed
    'Employment_Status_Self_Employed': np.random.choice([0, 1], num_samples, p=[0.9, 0.1]),
    'Employment_Status_Unemployed': np.random.choice([0, 1], num_samples, p=[0.95, 0.05]),
    'Housing_Status_Rent': np.random.choice([0, 1], num_samples, p=[0.6, 0.4]), # Mix of rent/own
    'Housing_Status_Own': np.random.choice([0, 1], num_samples, p=[0.4, 0.6]),
}

df = pd.DataFrame(data)

# Ensure one employment status is 1 and others 0
def set_employment_status(row):
    status_type = np.random.choice(['Employed', 'Self_Employed', 'Unemployed'], p=[0.8, 0.15, 0.05])
    row['Employment_Status_Employed'] = 0
    row['Employment_Status_Self_Employed'] = 0
    row['Employment_Status_Unemployed'] = 0
    if status_type == 'Employed':
        row['Employment_Status_Employed'] = 1
    elif status_type == 'Self_Employed':
        row['Employment_Status_Self_Employed'] = 1
    else:
        row['Employment_Status_Unemployed'] = 1
    return row

df = df.apply(set_employment_status, axis=1)

# Ensure one housing status is 1 and others 0
def set_housing_status(row):
    status_type = np.random.choice(['Rent', 'Own'], p=[0.5, 0.5])
    row['Housing_Status_Rent'] = 0
    row['Housing_Status_Own'] = 0
    if status_type == 'Rent':
        row['Housing_Status_Rent'] = 1
    else:
        row['Housing_Status_Own'] = 1
    return row

df = df.apply(set_housing_status, axis=1)


# --- 2. Create Target Variable (Approval Status) ---
# This is a simplified logic to assign 'Approved' (1) or 'Rejected' (0)
# based on a combination of features. This simulates the decision-making
# process a real credit card company might use.

df['Approved'] = 0 # Default to rejected

# Conditions for approval (simplified for synthetic data)
# Higher credit score, higher income, lower DTI, stable employment generally lead to approval.
df.loc[
    (df['Credit_Score'] >= 650) &
    (df['Income'] >= 40000) &
    (df['Debt_to_Income_Ratio'] <= 0.4) &
    (df['Employment_Years'] >= 2) &
    (df['Employment_Status_Employed'] == 1),
    'Approved'
] = 1

df.loc[
    (df['Credit_Score'] >= 700) &
    (df['Income'] >= 60000) &
    (df['Debt_to_Income_Ratio'] <= 0.5) &
    (df['Employment_Years'] >= 1) &
    (df['Employment_Status_Self_Employed'] == 1),
    'Approved'
] = 1

# Introduce some noise/exceptions for more realistic data
# Some good candidates might be rejected, some less ideal might be approved
num_noise = int(num_samples * 0.1) # 10% noise
noise_indices = np.random.choice(df.index, num_noise, replace=False)
df.loc[noise_indices, 'Approved'] = 1 - df.loc[noise_indices, 'Approved'] # Flip approval status

print("--- Synthetic Data Sample ---")
print(df.head())
print(f"\nApproval Distribution:\n{df['Approved'].value_counts()}")

# --- 3. Prepare Data for Model Training ---
X = df.drop('Approved', axis=1)
y = df['Approved']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"\nTraining set shape: {X_train.shape}")
print(f"Testing set shape: {X_test.shape}")

# --- 4. Train the Machine Learning Model (Random Forest Classifier) ---
# Random Forest is chosen for its complexity and good performance on tabular data.
print("\n--- Training Random Forest Classifier ---")
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)
print("Model training complete.")

# --- 5. Evaluate the Model ---
y_pred = model.predict(X_test)

print("\n--- Model Evaluation ---")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# --- 6. Save the Trained Model ---
# This model file would then be loaded by your backend server (e.g., Flask, FastAPI)
# to make predictions based on user input from the frontend.
model_filename = 'credit_approval_model.joblib'
joblib.dump(model, model_filename)
print(f"\nModel saved as {model_filename}")

# --- 7. Print Feature Names (useful for frontend input mapping) ---
print("\n--- Feature Names for Frontend Mapping ---")
print(X.columns.tolist())

