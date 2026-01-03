🏦 AI Mortgage Underwriting System

A production style AI-powered mortgage underwriting platform that combines rule-based credit logic, machine learning risk prediction, and model explainability(SHAP) - exposed via a FastAPI backend with an interactive Streamlit dashboard.

🚀 Features


✅ Rule-Based underwriting engine (credit score, LTV,DTI,employment)
🤖 Machine Learning default risk prediction(Logistic Regression)
📊 SHAP explainability (feature attribution & decision breakdown)
🌐 FASTAPI REST API
🖥️ Streamlit Dashboard for live simulation
♻️ Hybrid decision system (Rules + ML)
📦 Model persistance and interface pipeline


📊 Decision Logic

Rule Based Factors
-Credit Score
-Loan to Value
-Debt to Income
-Down Payment
-Employment Status

ML Model
-Logisitic Regression
-Synthetic training data
-Outputs:
-Default class (0/1)
-Default probability

Final Decision

Condition              Outcome
High Risk              Denied
Moderate Risk          Refer/Conditional
Low Risk               Approved

SHAP Explainability
-Feature Importance visualization
-Borrower Specific Breakdown
-Transparent ML decision support (enterprise-Grade)

🧪 Example API request
Post Underwrite
{
    "annual_income": 85000,
    "credit_score": 720,
    "monthly_debt": 1200,
    "loan_amount": 300000,
    "property_value": 420000,
    "employment_status": "employed"
}

📦 Tech Stack

Backend
-FASTAPI
-Pydantic
-Uvicorn

Machine Learning
-scikit-learn
-pandas/numpy
-SHAP
-joblib

Frontend
-Streamlit

⚙️Setup Instructions

pyhton -m venv venv
source venv/bin/activate

Install Dependencies
pip install -r requirements.txt

Train ML Model
python -m ml.train_model

Start API
uvicorn app.main:app --reload

Run Dashboard
streamlit run dashboard.py

Future Improvements 🔮
-Support additional ML models 
-Persist Underwriting decisions in a database
-Integrate authentication and role based access control
-Synthetic training data converted with historical loan data

License 

MIT License

Deployment

-Backend: Dockerized FastAPI service
-Frontend: Streamlit Dashboard
-Deployed using container based cloud infrastructure

Both services run independently and communicate over HTTP.








