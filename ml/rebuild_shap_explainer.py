import joblib
import shap
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "mortgage_underwriter_model.pkl"
SHAP_PATH = BASE_DIR / "shap_explainer.pkl"

print("Rebuilding SHAP explainer (LinearExplainer)...")


model = joblib.load(MODEL_PATH)


preprocessor = model.named_steps["preprocessor"]
classifier = model.named_steps["classifier"]  


background_raw = pd.DataFrame([{
    "credit_score": 700,
    "loan_amount": 250000,
    "property_value": 400000,
    "monthly_income": 6000,
    "monthly_debt": 1200,
    "employment_status": "employed"
}])

background_transformed = preprocessor.transform(background_raw)


explainer = shap.LinearExplainer(
    classifier,
    background_transformed,
    feature_perturbation="interventional"
)


joblib.dump(explainer, SHAP_PATH)

print("SHAP LinearExplainer rebuilt successfully")
print(f"Saved to: {SHAP_PATH}")


