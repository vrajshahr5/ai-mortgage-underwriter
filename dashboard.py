import streamlit as st
import requests
import shap
import matplotlib.pyplot as plt
import joblib
import pandas as pd
import os

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
        raise RuntimeError("API_URL environment variable not set.")

    response = requests.post(f"{API_URL}/underwrite", json=payload, timeout=60)

    st.subheader("Underwriting Result")
    if response.status_code == 200:
        result = response.json()
        st.success(f"Decision: **{result['decision'].upper()}**")
        st.write(f"Risk Score: {result.get('risk_score', 'N/A')}")
        st.write("### Reasons / Factors:")
        st.json(result["reasons"])

        if result["conditions"]:
            st.warning("### Conditions for Approval:")
            st.json(result["conditions"])

        st.write("### Full Explanation:")
        st.json(result["explanation"])

        if "ml_default_probability" in result["explanation"]:
            ml_prob = result["explanation"]["ml_default_probability"]
            st.metric(label="ML Predicted Default Probability", value=f"{ml_prob*100:.2f}%")
        

    
        st.subheader("Model Explanation (SHAP)")

        try:
            explainer = joblib.load("ml/shap_explainer.pkl")
            model = joblib.load("ml/mortgage_underwriter_model.pkl")

            input_df = pd.DataFrame([{
                "credit_score": credit_score,
                "loan_amount": loan_amount,
                "property_value": property_value,
                "monthly_income": annual_income / 12,
                "monthly_debt": monthly_debt,
                "employment_status": employment_status
            }])

            processed = model["preprocessor"].transform(input_df)
            shap_values = explainer(processed)

            
            st.write("### Feature Importance (Model Behaviour)")
            fig1, ax1 = plt.subplots()
            shap.summary_plot(shap_values[:,:,1],show=False)
            st.pyplot(fig1)
            plt.close(fig1)

        
            st.write("### Why This Decision? (Borrower Specific)")
            single_shap = shap_values[0,:,1] 
            
            fig2, ax2 = plt.subplots()
            shap.plots.waterfall(single_shap, show=False)
            st.pyplot(fig2)
            plt.close(fig2)

        except Exception as e:
            st.error(f"Waterfall SHAP Error: {e}")

    else:   
        st.error(f"Request Failed: {response.status_code}")
        st.write(response.text)

