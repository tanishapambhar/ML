from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pathlib import Path
import os
import joblib
import pandas as pd

app = FastAPI(
    title="Vehicle Insurance Fraud Detection API",
    description="Machine learning API for detecting fraudulent vehicle insurance claims",
    version="1.0.0"
)

# Enable CORS for frontend applications (local development + production support)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve model path dynamically regardless of execution directory
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR.parent / "model" / "vehicle_fraud_pipeline.pkl"

if not MODEL_PATH.exists():
    fallback_paths = [
        BASE_DIR.parent.parent / "vehicle_fraud_pipeline.pkl",
        Path("BACKEND/ml/model/vehicle_fraud_pipeline.pkl"),
        Path("BACKEND/vehicle_fraud_pipeline.pkl"),
        Path("ml/model/vehicle_fraud_pipeline.pkl"),
        Path("vehicle_fraud_pipeline.pkl"),
    ]
    for p in fallback_paths:
        if p.exists():
            MODEL_PATH = p
            break

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model file 'vehicle_fraud_pipeline.pkl' not found at {MODEL_PATH}")

print(f"Loading vehicle fraud detection pipeline from: {MODEL_PATH}")
model = joblib.load(MODEL_PATH)
print("Pipeline loaded successfully!")


class VehicleData(BaseModel):
    age_of_driver: int = Field(..., ge=0, description="Age of the driver")
    safety_rating: int = Field(..., ge=0, le=100, description="Safety rating (0-100)")
    annual_income: float = Field(..., ge=0, description="Annual income")
    high_education: int = Field(..., description="1 for Yes, 0 for No")
    address_change: int = Field(..., description="1 for Yes, 0 for No")
    property_status: str = Field(..., description="Own, Rent, or Mortgaged")
    claim_date: str = Field(..., description="Date formatted as M/D/YYYY or MM/DD/YYYY")
    claim_day_of_week: str = Field(..., description="Day name (e.g., Monday)")
    accident_site: str = Field(..., description="Urban, Rural, Highway, or local")
    past_num_of_claims: int = Field(..., ge=0, description="Past number of claims")
    witness_present: int = Field(..., description="1 for Yes, 0 for No")
    liab_prct: float = Field(..., ge=0, le=100, description="Liability percentage (0-100)")
    channel: str = Field(..., description="Filing channel: Online, Agent, Broker, Phone")
    police_report: int = Field(..., description="1 for Yes, 0 for No")
    age_of_vehicle: int = Field(..., ge=0, description="Age of vehicle in years")
    vehicle_category: str = Field(..., description="Small, Medium, Large, Luxury")
    vehicle_price: float = Field(..., ge=0, description="Vehicle price")
    total_claim: float = Field(..., ge=0, description="Total claim amount")
    injury_claim: float = Field(..., ge=0, description="Injury claim amount")
    policy_deductible: float = Field(..., ge=0, description="Policy deductible")
    annual_premium: float = Field(..., ge=0, description="Annual premium")
    days_open: float = Field(..., ge=0, description="Days open")
    form_defects: int = Field(..., ge=0, description="Number of form defects")


@app.get("/")
def home():
    return {
        "message": "Vehicle Fraud Detection API is running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs"
        }
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "classes": [int(c) for c in model.classes_] if hasattr(model, "classes_") else []
    }


@app.post("/predict")
def predict(data: VehicleData):
    try:
        input_data = pd.DataFrame([
            {
                "age_of_driver": data.age_of_driver,
                "safety_rating": data.safety_rating,
                "annual_income": data.annual_income,
                "high_education": data.high_education,
                "address_change": data.address_change,
                "property_status": data.property_status,
                "claim_date": data.claim_date,
                "claim_day_of_week": data.claim_day_of_week,
                "accident_site": data.accident_site,
                "past_num_of_claims": data.past_num_of_claims,
                "witness_present": data.witness_present,
                "liab_prct": data.liab_prct,
                "channel": data.channel,
                "police_report": data.police_report,
                "age_of_vehicle": data.age_of_vehicle,
                "vehicle_category": data.vehicle_category,
                "vehicle_price": data.vehicle_price,
                "total_claim": data.total_claim,
                "injury_claim": data.injury_claim,
                "policy deductible": data.policy_deductible,
                "annual premium": data.annual_premium,
                "days open": data.days_open,
                "form defects": data.form_defects
            }
        ])

        prediction = int(model.predict(input_data)[0])
        result = "Fraud" if prediction == 1 else "Not Fraud"

        fraud_probability = 100.0 if prediction == 1 else 0.0
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_data)[0]
            # Probability of Class 1 (Fraud)
            fraud_probability = round(float(probabilities[1]) * 100, 2)

        return {
            "prediction": prediction,
            "result": result,
            "probability": fraud_probability
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)