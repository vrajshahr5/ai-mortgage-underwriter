from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import shap


from ml.data_generator import generate_synthetic_data

categorical_features = ["employment_status"]

data_frame = generate_synthetic_data(5000)

model_X = data_frame.drop("default_risk", axis=1)
model_Y = data_frame["default_risk"]

X_train, X_test, y_train, y_test = train_test_split(model_X, model_Y, test_size = 0.2, random_state=42)

numeric_features = ["credit_score", "loan_amount", "property_value", "monthly_income","monthly_debt"]
categorical_features = ["employment_status"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat",OneHotEncoder(),categorical_features)
    ]
)

model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression())
])

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, y_pred))

explainer = shap.Explainer(model.predict, X_train)

X_train_processed = model.named_steps["preprocessor"].transform(X_train)

explainer = shap.Explainer(model.named_steps["classifier"].predict_proba, X_train_processed)

shap_values = explainer(X_train_processed)

joblib.dump(explainer, "ml/shap_explainer.pkl")
print("SHAP Explanainer saved successfully.")


joblib.dump(model, "ml/mortgage_underwriter_model.pkl")
print("Model saved successfully.")











