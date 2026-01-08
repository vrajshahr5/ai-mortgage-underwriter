from app.schemas import MortgageApplicationCreate,UnderWritingDecisionResponse
from pathlib import Path
import pandas as pd
import joblib


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "ml" / "mortgage_underwriter_model.pkl"
SHAP_PATH = BASE_DIR / "ml" / "shap_explainer.pkl"


model = joblib.load(MODEL_PATH)
shap_explainer = joblib.load(SHAP_PATH)


def evaluate_application(application: MortgageApplicationCreate):

    risk_score = 0
    reasons = []
    approval_factors = []
    conditions = []
    explanation = {}

    ltv = application.loan_amount / application.property_value
    dti = application.monthly_debt / (application.annual_income / 12)
    down_payment = application.property_value - application.loan_amount

    if application.credit_score <600:
        risk_score += 50
        reasons.append("Credit score below 600")
    elif application.credit_score <700:
        risk_score += 20
        reasons.append("credit score between 600 and 699")
    else:
        approval_factors.append("Strong credit score")
    if ltv > 0.8:
        risk_score += 30
        reasons.append("High loan-to-value ratio")
    else:
        approval_factors.append("Conservative loan-to-value ratio")
    if dti > 0.4:
        risk_score += 20
        reasons.append("High debt to income ratio")
    else:
        approval_factors.append("Low debt to income ratio")
    if down_payment < 20000:
        risk_score += 10
        reasons.append("Down payment less than $20,000")
    if application.employment_status == "unemployed":
        risk_score += 15
        reasons.append("unemployed applicant")
    elif application.employment_status == "self_employed":
        risk_score += 5
        reasons.append("Self-employed applicant-income stability uncertain")
    else:
        approval_factors.append("Stable employment")
    
    
    if risk_score >= 50:
        decision = "denied"
        explanation = {"decision_logic": "Risk score exceeded denial threshold"}
    elif risk_score >=25:
        decision = "refer"
        conditions.append("verify income and employment status")
        explanation = {"decision_logic": "Moderate risk score - manual review required"}
    else:
        decision = "approved"
        explanation = {"approval_factors": approval_factors}
    return UnderWritingDecisionResponse(
        decision=decision,
        risk_score=risk_score,
        reasons=reasons,
        conditions=conditions,
        explanation=explanation
    )

def predict_default_risk_ml(application):
    input_df = pd.DataFrame([{
        "credit_score": application.credit_score,
        "loan_amount": application.loan_amount,
        "property_value": application.property_value,
        "monthly_income": application.annual_income / 12,
        "monthly_debt": application.monthly_debt,
        "employment_status": application.employment_status
    }])

    class_prediction = int(model.predict(input_df)[0]) 
    prob_default = float(model.predict_proba(input_df)[0][1])

    return class_prediction, prob_default

def explain_with_shap(application: MortgageApplicationCreate):
    """
    Returns SHAP values mapped to transformed feature names
    """
    input_df = pd.DataFrame([{
        "credit_score": application.credit_score,
        "loan_amount": application.loan_amount,
        "property_value": application.property_value,
        "monthly_income": application.annual_income / 12,
        "monthly_debt" : application.monthly_debt,
        "employment_status": application.employment_status
    }])

    preprocessor = model.named_steps["preprocessor"]
    input_transformed = preprocessor.transform(input_df)

    shap_values = shap_explainer(input_transformed)
    feature_names = preprocessor.get_feature_names_out()

    return {
        feature: float(value)
        for feature, value in zip(feature_names, shap_values.values[0])
    }

def summarize_shap_explanation(shap_explanation, top_k=3):
    """
    Returns top-k SHAP features by absolute impact
    """
    return sorted(
        shap_explanation.items(),
        key=lambda item: abs(item[1]),
        reverse=True
    )[:top_k]

FEATURE_TEXT = {
    "num_credit_score": "Low credit score significantly increased risk.",
    "num_monthly_debt": "High monthly debt increased default probability.",
    "num_monthly_income": "Lower income increased risk.",
    "num_loan_amount": "loan amount increased risk.",
    "cat_employment_staus_status_self-employed": "Unemployment status impacted risk.",
    "cat_employment_status_employed": "Stable employment reduced risk."
}

def build_shap_explanation_text(shap_explantion):
    """
    Converts SHAP values into human readable text explanations
    """
    top_features = summarize_shap_explanation(shap_explantion)

    explanations = []
    for feature, value in top_features:
        text = FEATURE_TEXT.get(feature, f"Feature {feature}  had a significant impact on the decision.")
        explanations.append(text)

    return explanations


def evaluate_with_ml(application: MortgageApplicationCreate):
    rule_result = evaluate_application(application)
    class_predicition, prob_default = predict_default_risk_ml(application)
    shap_explanation =explain_with_shap(application)
    human_explanation = build_shap_explanation_text(shap_explanation)

    
    return UnderWritingDecisionResponse(
        decision=rule_result.decision,
        reasons = rule_result.reasons,
        risk_score=rule_result.risk_score,
        conditions=rule_result.conditions,
        explanation={
            "rule_engine": rule_result.explanation,
            "ml_default_probability": prob_default,
            "ml_predicted_risk_class": class_predicition,
            "shap_explanation": shap_explanation,
            "explanation_text": human_explanation
        }

    )


















 








    
  


    
   
    




    



    











