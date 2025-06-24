 <h1> CardWise: Smart Credit Card Approval Predictor </h1>

CardWise is an interactive web application that predicts credit card approval status. It uses an intelligent machine learning model to assess user-provided financial and personal data, offering instant and clear feedback on eligibility. This project demonstrates a ML application, integrating a dynamic frontend with a Python-based prediction service.

<picture>
 <a href="https://ibb.co/twS41djC"><img src="https://i.ibb.co/35w7PJ6h/Screenshot-2025-06-21-223426.png" alt="Screenshot-2025-06-21-223426" border="0" /></a>
 <img alt="HOME PAGE" src="YOUR-DEFAULT-IMAGE">
</picture>

<picture>
<a href="https://ibb.co/nqxcDcP4"><img src="https://i.ibb.co/6cjP4PXG/Screenshot-2025-06-21-222006.png" alt="Screenshot-2025-06-21-222006" border="0" /></a>
 <img alt="HOME PAGE" src="YOUR-DEFAULT-IMAGE">
</picture>

  <h2>Credit Card Approval Flow</h2>
  <ul>
    <li><strong>Welcome Screen:</strong> You start on the app's home page.</li>
    <li><strong>Go to Form:</strong> You navigate to the credit card application form.</li>
    <li><strong>Fill Details:</strong> You enter your personal and financial information.</li>
    <li><strong>Submit:</strong> You click to check your approval status.</li>
    <li><strong>Data Sent:</strong> Your info is sent to a Python server.</li>
    <li><strong>Data Processed:</strong> The server cleans and transforms your raw input data (e.g., converting categories to numbers, calculating ratios).</li>
    <li><strong>Random Forest Predicts:</strong> A Random Forest Classifier (an advanced machine learning algorithm made of many decision trees) analyzes the processed data based on patterns it learned from past applications.</li>
    <li><strong>Result Shown:</strong> The app instantly displays your approval status (green for approved, red for denied) with a reason, based on the Random Forest's decision.</li>
    <li><strong>Reset:</strong> You can clear the form to try again.</li>
  </ul>

  <picture>
 <a href="https://ibb.co/czg0ZSb"><img src="https://i.ibb.co/Tzv67xK/Screenshot-2025-06-21-223536.png" alt="Screenshot-2025-06-21-223536" border="0" /></a>
 <img alt="HOME PAGE" src="YOUR-DEFAULT-IMAGE">
</picture>

## Tech Stack

* **Frontend:**
    * **HTML5:** Structure.
    * **CSS3:** Styling, utilizing [Tailwind CSS](https://tailwindcss.com/).
    * **JavaScript :** Interactivity, validation, and communication.
* **Backend (Conceptual ML Service):**
    * **Python 3.x:** Core language for ML logic.
    * **scikit-learn:** Implements the **Random Forest Classifier** algorithm.
    * **pandas:** Data preprocessing.
    * **joblib:** Model saving/loading.
    * **Flask & Flask-CORS:** (Conceptual) HTTP service to expose the ML model.

To get CardWise running locally:

### Prerequisites

* Python 3.x (with `pip`)
* `git`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/RhythmRhythmm/CardWise.git](https://github.com/RhythmRhythmm/CardWise.git)
    cd CardWise
    ```
2.  **Create & activate a virtual environment:**
    ```bash
    python -m venv venv
    # Windows: .\venv\Scripts\activate
    # macOS/Linux: source venv/bin/activate
    ```
3.  **Install dependencies (create `requirements.txt` first if missing):**
    ```
    Flask==2.3.2
    Flask-Cors==3.0.10
    joblib==1.3.2
    pandas==2.0.3
    scikit-learn==1.3.0
    numpy==1.25.2
    ```
    Then: `pip install -r requirements.txt`
4.  **Train the ML Model:**
    ```bash
    python ml_model_training.py
    ```
    This creates `credit_approval_model.joblib`.
5.  **Run the Backend Service:**
    ```bash
    python app.py
    ```
    The server typically starts on `http://127.0.0.1:5000/`.
6.  **Open Frontend:**
    Open `index.html` in your web browser.


