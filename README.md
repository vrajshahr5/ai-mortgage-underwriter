AI Mortgage Underwriter
Overview
AI Mortgage Underwriter is a production-style, AI-powered mortgage underwriting platform that combines deterministic credit rules, a machine-learning risk model, and SHAP-based explainability.

The system is exposed through a FastAPI backend and evaluated using an interactive Streamlit dashboard, simulating a realistic automated underwriting workflow suitable for enterprise or fintech environments.

This project emphasizes decision transparency, model governance, and system architecture, not just prediction accuracy.

Key Features
Hybrid Decision System
Combines rule-based underwriting logic with machine-learning risk prediction

Ensures deterministic business rules remain enforceable alongside probabilistic models

Rule-Based Underwriting Engine
Evaluates borrower risk using:

Credit score

Loan-to-Value (LTV)

Debt-to-Income (DTI)

Minimum down payment

Employment stability

Machine Learning Default Risk Model
Algorithm: Logistic Regression

Training Data: 5,000 synthetic mortgage applications

Outputs:

Default risk class

Probability of default

Feature-level SHAP attributions

Explainable AI (XAI)
SHAP-based feature attribution for every prediction

Human-readable explanation summaries generated server-side

Supports model transparency and regulatory review workflows

REST API Backend
Built with FastAPI

Strong input validation using Pydantic

Stateless JSON-based inference indication

Interactive Frontend
Streamlit dashboard for real-time evaluation

Frontend consumes API outputs only (no client-side ML)

Designed for demos, audits, and stakeholder review

Model Persistence & Reproducibility
Trained models, preprocessors, and SHAP explainers serialized using joblib

Deterministic inference across environments

Extensible Architecture
Modular design supports:

Additional models

Real datasets

Alternative decision policies

Enterprise scaling patterns

Rule-Based Decision Logic
Risk Score	Decision
≥ 50	Application Denied
25 – 49	Refer / Conditional Approval
< 25	Application Approved
Machine Learning Pipeline
Algorithm: Logistic Regression

Preprocessing:

Standard scaling (numerical features)

One-hot encoding (categorical features)

Explainability:

SHAP feature attribution

Human-readable explanation summaries

API Example
Endpoint
POST /underwrite
Sample Request
{
  "annual_income": 85000,
  "credit_score": 720,
  "monthly_debt": 1200,
  "loan_amount": 300000,
  "property_value": 420000,
  "employment_status": "employed"
}
Sample Response
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
Technology Stack
Backend
FastAPI

Pydantic

Uvicorn

Joblib

Machine Learning
Scikit-learn

Pandas

NumPy

SHAP

ColumnTransformer & Pipelines

Frontend
Streamlit

REST integration via requests

Setup & Usage
Clone Repository
git clone https://github.com/vrajshahr5/AI-Mortgage-Underwriter.git
cd AI-Mortgage-Underwriter
Create Virtual Environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
Install Dependencies
pip install -r requirements.txt
Train ML Model
python -m ml.train_model
Start Backend
uvicorn app.main:app --reload
Run Frontend
streamlit run dashboard.py
Project Structure
AI-Mortgage-Underwriter/
├── app/
│   ├── main.py
│   ├── schemas.py
│   └── underwriting_engine.py
├── ml/
│   ├── train_model.py
│   ├── rebuild_shap_explainer.py
│   ├── mortgage_underwriter_model.pkl
│   └── shap_explainer.pkl
├── dashboard.py
└── requirements.txt
Deployment
Backend and frontend are independently deployable

Communication via HTTPS REST API

Deployed using Docker-based infrastructure on Render

Live Endpoints
FastAPI Backend:
https://ai-mortgage-underwriter.onrender.com

Streamlit Dashboard:
https://ai-mortgage-underwriter-dashboard.onrender.com

Note: The hosted demo uses a free tier deployment. Under heavier traffic, rate-limiting may occur due to compute-intensive SHAP generation. The system operates without limitation in local or production-grade environments.

Why This Project Matters
This project demonstrates:

Applied machine learning in a regulated domain

Hybrid decision system design

Explainable AI implementation

Production-style API architecture

Frontend-backend separation

Model governance considerations
























