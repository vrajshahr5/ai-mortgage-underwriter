from app.schemas import MortgageApplicationCreate,UnderWritingDecisionResponse
import pandas as pd
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml" / "mortgage_underwriter_model.pkl"

model = joblib.load(MODEL_PATH)

def evaluate_application(application: MortgageApplicationCreate):

    risk_score = 0
    reasons = []
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
    if ltv > 0.8:
        risk_score += 30
        reasons.append("High loan-to-value ratio")
    if dti > 0.4:
        risk_score += 20
        reasons.append("High debt to income ratio")
    if down_payment < 20000:
        risk_score += 10
        reasons.append("Down payment less than $20,000")
    if application.employment_status == "unemployed":
        risk_score += 15
        reasons.append("unemployed applicant")
    elif application.employment_status == "self_employed":
        risk_score += 5
        reasons.append("Self-employed applicant-income stability uncertain")
    
    
    if risk_score >= 50:
        decision = "denied"
        explanation = {"reason": reasons}
    elif risk_score >=25:
        decision = "refer"
        conditions.append("verify income and status")
        explanation = {"conditions": conditions, "factors": reasons}
    else:
        decision = "approved"
        explanation = {"factors": reasons}
    return UnderWritingDecisionResponse(
        decision=decision,
        risk_score=risk_score,
        reasons=reasons,
        conditions=conditions,
        explanation=explanation
    )

def predict_default_risk_ml(application):
    input_data = pd.DataFrame([{
        "credit_score": application.credit_score,
        "loan_amount": application.loan_amount,
        "property_value": application.property_value,
        "monthly_income": application.annual_income / 12,
        "monthly_debt": application.monthly_debt,
        "employment_status": application.employment_status
    }])

    class_prediction = int(model.predict(input_data)[0]) 
    prob_default = float(model.predict_proba(input_data)[0][1])

    return class_prediction, prob_default


def evaluate_with_ml(application: MortgageApplicationCreate):
    rule_result = evaluate_application(application)
    class_predicition, prob_default = predict_default_risk_ml(application)

   

    return UnderWritingDecisionResponse(
        decision=rule_result.decision,
        reasons = rule_result.reasons,
        risk_score=rule_result.risk_score,
        conditions=rule_result.conditions,
        explanation={
            "rule_engine": rule_result.explanation,
            "ml_default_probability": prob_default,
            "ml_predicted_risk_class": class_predicition
        }

    )














 








    
  


    
   
    




    



    











