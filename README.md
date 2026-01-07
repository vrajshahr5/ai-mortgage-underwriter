AI Mortgage Underwriter
-
A production style AI powered mortgage underwriting platform that combines deterministic credit rules, a machine learning risk model, and SHAP based explainability. The system is exposed thorugh a FastAPI backend and evaluated using an interactive Streamlit dashboard.

The goal of this project is to provide a realistic simulation of an automated underwriting workflow suitable for enterprise or fintech enviornments.

Key Features 
-
Hybrid Decision System Integrates rule based logic with ML predictions,
Rule based Underwriting engine Evaluates credit score, LTV, DTI, down payement and employment stability,
Machine Learning Default Risk Predicition Logistic Regression model trained on synthetic borrower data,
Model Explainabilty Shap visualizations show feature contributions of each borrower,
Rest API backend FastAPI service for standardized evaluations,
Interactive Frontend Streamlit dashboard for real time demonstration,
Model Persistance Trained models and preprocessors are serialized with joblib,
Extensible Architecture Designed to support additonal models or real datasets in the future.

The deterministic engine calculates and applies risk adjustments based on:
- 
+ Credit Score 
+ Loan to Value ratio
+ Debt to income ratio
+ Minimum down payment
+ Employment status

| Risk Score Range | Result                          |
|------------------|---------------------------------|
| ≥ 50             | Application Denied              |
| 25 – 49          | Refer / Conditional Approval    |
| < 25             | Application Approved            |

Machine Learning Model
-
Algorithm Logistic Regression
Training Data 5000 synthetic mortgage applications
Preprocessing Standard scaling for numeric inputs and one hot encoding for categorical inputs
Outputs Default risk class, Probability of Default, SHAP feature attributions.

API Example
-
POST /underwrite

**Sample Request**

```json
{
    "annual_income": 85000,
    "credit_score": 720,
    "monthly_debt": 1200,
    "loan_amount": 300000,
    "property_value": 420000,
    "employment_status": "employed"
}
```

**Sample Response**

```json
{
    "decision": "approved",
    "risk_score": 22,
    "reasons": ["Credit score between 700 and 749"],
    "conditions": [],
    "explanation": {
        "rule_engine": { "...": "details omitted" },
        "ml_default_probability": 0.07
    }
}
```

---

Technology Stack
-
+ FastAPI
+ Pydantic Models
+ Uvicorn
+ Joblib

Machine Learning
-
+ scikit-learn
+ Pandas and Numpy
+ SHAP
+ Column Transformer and Pipeline

Frontend
-
+ Streamlit
+ HTTP integration with requests

Setup and Usage
-
Clone the repository:

```bash
git clone https://github.com/vrajshahr5/AI-Mortgage-Underwriter.git
cd AI-Mortgage-Underwriter
```
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Train the ML model:

```bash
python -m ml.train_model
```

Start the FastAPI backend:

```bash
uvicorn app.main:app --reload
```

Run the Streamlit dashboard:

```bash
streamlit run dashboard.py
```

---

Project Structure
-![IMG_3661](https://github.com/user-attachments/assets/53313a9f-5dcf-4459-a908-998fdf2bc2dd)

Deployment
-
https://ai-mortgage-underwriter.onrender.com
https://ai-mortgage-underwriter-dashboard.onrender.com






















