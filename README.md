AI Mortgage UnderWriter
-
Overview
-
AI Mortgage Underwriter is a production-style, AI-powered mortgage underwriting platform that combines deterministic credit rules, a machine-learning risk model, and SHAP-based explainability.

The system is exposed through a FastAPI backend and evaluated using an interactive Streamlit dashboard, simulating a realistic automated underwriting workflow suitable for enterprise or fintech environments.

This project emphasizes decision transparency, model governance, and system architecture, not just prediction accuracy.

Key Features
-
+ Hybrid Decision System
+ Combines rule-based underwriting logic with machine-learning risk prediction
+ Ensures deterministic business rules remain enforceable alongside probabilistic models

Rule-Based Underwriting Engine
-
Evaluates borrower risk using:

+ Credit score
+ Loan-to-Value (LTV)
+ Debt-to-Income (DTI)
+ Minimum down payment
+ Employment stability

Machine Learning Default Risk Model
-
+ Algorithm: Logistic Regression
+ Training Data: 5,000 synthetic mortgage applications

 Outputs
 -
+ Default risk class

+ Probability of default

+ Feature-level SHAP attributions

Explainable AI
-

+ SHAP-based feature attribution for every prediction

+ Human-readable explanation summaries generated server-side

+ Supports model transparency and regulatory review workflows

REST API Backend
-

+ Built with FastAPI

+ Strong input validation using Pydantic

+ Stateless JSON-based inference indication

Interactive Frontend
-

+ Streamlit dashboard for real-time evaluation

+ Frontend consumes API outputs only (no client-side ML)

+ Designed for demos, audits, and stakeholder review

Model Persistence & Reproducibility
-

+ Trained models, preprocessors, and SHAP explainers serialized using joblib

+ Deterministic inference across environments

Extensible Architecture
-

+ Modular design supports

+ Additional models

+ Real datasets

+ Alternative decision policies

+ Enterprise scaling patterns

Rule Based Decision Logic
-
| Category | Condition | Risk Score Adjustment |
|---------|-----------|-----------------------|
| Credit Score | < 600 | +50 |
| Credit Score | 600–699 | +20 |
| Credit Score | ≥ 700 | 0 |
| Loan-to-Value (LTV) | > 80% | +30 |
| Loan-to-Value (LTV) | ≤ 80% | 0 |
| Debt-to-Income (DTI) | > 40% | +20 |
| Debt-to-Income (DTI) | ≤ 40% | 0 |
| Down Payment | < $20,000 | +10 |
| Employment Status | Unemployed | +15 |
| Employment Status | Self-employed | +5 |
| Employment Status | Employed | 0 |


| Total Risk Score | Underwriting Decision |
|------------------|----------------------|
| ≥ 50 | Denied |
| 25 – 49 | Refer / Manual Review |
| < 25 | Approved |

Machine Learning Pipeline
-

Algorithm: Logistic Regression

Preprocessing
-

+ Standard scaling (numerical features)

+ One-hot encoding (categorical features)

Explainability
-
+ SHAP feature attribution

+ Human-readable explanation summaries

API Example
-

## API Example

### Sample Request

```json
{
  "annual_income": 100000,
  "credit_score": 720,
  "monthly_debt": 800,
  "loan_amount": 200000,
  "property_value": 450000,
  "employment_status": "employed"
}

```









