from fastapi import FastAPI
from app.schemas import MortgageApplicationCreate,UnderWritingDecisionResponse
from app.underwriting_engine import evaluate_with_ml

app = FastAPI(
    title="Mortgage Underwriting API",
    description="API for processing mortgage applications and providing underwriting decisions."
    )
@app.post("/underwrite", response_model=UnderWritingDecisionResponse)
def underwrite_application(application: MortgageApplicationCreate):
    return evaluate_with_ml(application)

@app.get("/")
def root():
    return {"message": "API Mortgage Underwriting Service is running."}

















   
    



