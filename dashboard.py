import streamlit as st
import requests
import pandas as pd
import os

st.set_page_config(page_title="AI Mortgage Underwriting Dashboard", layout = "centered")
st.title("AI Mortgage Underwriting Dashboard")
st.write("Enter borrower details to get an underwriting evaluation.")
st.subheader("Borrower Information")

annual_income = st.number_input("Annual Income($)", min_value=0)
credit_score = st.slider("Credit Score", min_value = 300, max_value=850)
monthly_debt = st.number_input("Monthly Debt($)", min_value=0)
loan_amount = st.number_input("loan Amount($)",min_value=0)
property_value = st.number_input("Property Value($)", min_value=0)

employment_status = st.selectbox("Employment Status", options=["employed", "unemployed", "self-employed"])

if st.button("Evaluate Application"):
    payload={
        "annual_income": annual_income,
        "credit_score": credit_score,
        "monthly_debt": monthly_debt,
        "loan_amount": loan_amount,
        "property_value": property_value,
        "employment_status": employment_status
    }

    API_URL = os.getenv("API_URL")
    if not API_URL:
        st.error("API_URL environment variable not set.")
        st.stop()
    
    with st.spinner("Evaluating application..."):
        response = requests.post(f"{API_URL}/underwrite/", json=payload,timeout=60)
      

    st.subheader("Underwriting Result")
    if response.status_code != 200:
        st.error(f"Request failed with status code ({response.status_code})")
        st.write(response.text)
        st.stop()

    result = response.json()

    decision = result["decision"].upper()
    risk_score = result.get("risk_score", "N/A")

    if decision == "APPROVED":
        st.success(f"Decision: {decision}")
    elif decision == "DENIED":
        st.error(f"Decision: {decision}")
    else:
        st.error(f"Decision: {decision}")

    st.write(f"Risk score: {risk_score}")

    st.subheader("Decision Rationale (Rules Engine)")

    rule_engine = result["explanation"].get("rule_engine", {})

    if decision == "APPROVED":
        factors = rule_engine.get("approval_factors", [])
        for f in factors:
            st.write(f"• {f}")

    elif decision == "REFER":
        st.write(rule_engine.get("decision_logic", "Manual review required."))
        if result["conditions"]:
            st.info("Conditions:")
            for c in result["conditions"]:
                st.write(f"• {c}")

    else:
        st.write(rule_engine.get("decision_logic", "High risk detected."))

    
    st.subheader("Machine Learning Risk Assessment")

    ml_prob = result["explanation"].get("ml_default_probability")
    if ml_prob is not None:
        st.metric(
            label="Predicted Probability of Default",
            value=f"{ml_prob * 100:.2f}%"
        )

    st.subheader("Why the Model Made This Prediction")

    explanation_text = result["explanation"].get("explanation_text", [])

    if explanation_text:
        for line in explanation_text:
            st.write(f"• {line}")
    else:
        st.write("No significant model drivers identified.")

   
    st.subheader("Feature Impact Overview")

    shap_data = result["explanation"].get("shap_explanation", {})
    if shap_data:
        df = pd.DataFrame(
            shap_data.items(),
            columns=["Feature", "Impact"]
        )
        st.bar_chart(df.set_index("Feature"))

   
    st.markdown("---")
    st.markdown("""
    **Model Governance**
    - Decision Type: Hybrid (Rules + Machine Learning)
    - Explainability: SHAP-based feature attribution
    - Human Review: Required for borderline cases
    - Deployment: API-driven inference (no client-side models)
    """)


