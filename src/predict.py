"""
FastAPI service for SWaT Intrusion Detection System.

This service loads a pre-trained model and provides a REST API
to classify sensor readings as Normal or Attack.
"""

import pickle

from fastapi import FastAPI
from pydantic import BaseModel, Field

# Load model artifacts
with open("dv.bin", "rb") as f_in:
    dv = pickle.load(f_in)

with open("model.bin", "rb") as f_in:
    model = pickle.load(f_in)

# Create FastAPI app
app = FastAPI(
    title="SWaT Intrusion Detection System",
    description="Real-time classification of water treatment system sensor readings",
    version="1.0.0",
)


# Define input schema for all 51 sensor features
class SensorReading(BaseModel):
    """Schema for SWaT sensor readings (51 features)."""

    FIT101: float = Field(..., description="Flow sensor 101")
    LIT101: float = Field(..., description="Level sensor 101")
    MV101: float = Field(..., description="Motor valve 101")
    P101: float = Field(..., description="Pump 101")
    P102: float = Field(..., description="Pump 102")
    AIT201: float = Field(..., description="Analyzer sensor 201")
    AIT202: float = Field(..., description="Analyzer sensor 202")
    AIT203: float = Field(..., description="Analyzer sensor 203")
    FIT201: float = Field(..., description="Flow sensor 201")
    MV201: float = Field(..., description="Motor valve 201")
    P201: float = Field(..., description="Pump 201")
    P202: float = Field(..., description="Pump 202")
    P203: float = Field(..., description="Pump 203")
    P204: float = Field(..., description="Pump 204")
    P205: float = Field(..., description="Pump 205")
    P206: float = Field(..., description="Pump 206")
    DPIT301: float = Field(..., description="Differential pressure sensor 301")
    FIT301: float = Field(..., description="Flow sensor 301")
    LIT301: float = Field(..., description="Level sensor 301")
    MV301: float = Field(..., description="Motor valve 301")
    MV302: float = Field(..., description="Motor valve 302")
    MV303: float = Field(..., description="Motor valve 303")
    MV304: float = Field(..., description="Motor valve 304")
    P301: float = Field(..., description="Pump 301")
    P302: float = Field(..., description="Pump 302")
    AIT401: float = Field(..., description="Analyzer sensor 401")
    AIT402: float = Field(..., description="Analyzer sensor 402")
    FIT401: float = Field(..., description="Flow sensor 401")
    LIT401: float = Field(..., description="Level sensor 401")
    P401: float = Field(..., description="Pump 401")
    P402: float = Field(..., description="Pump 402")
    P403: float = Field(..., description="Pump 403")
    P404: float = Field(..., description="Pump 404")
    UV401: float = Field(..., description="UV sensor 401")
    AIT501: float = Field(..., description="Analyzer sensor 501")
    AIT502: float = Field(..., description="Analyzer sensor 502")
    AIT503: float = Field(..., description="Analyzer sensor 503")
    AIT504: float = Field(..., description="Analyzer sensor 504")
    FIT501: float = Field(..., description="Flow sensor 501")
    FIT502: float = Field(..., description="Flow sensor 502")
    FIT503: float = Field(..., description="Flow sensor 503")
    FIT504: float = Field(..., description="Flow sensor 504")
    P501: float = Field(..., description="Pump 501")
    P502: float = Field(..., description="Pump 502")
    PIT501: float = Field(..., description="Pressure sensor 501")
    PIT502: float = Field(..., description="Pressure sensor 502")
    PIT503: float = Field(..., description="Pressure sensor 503")
    FIT601: float = Field(..., description="Flow sensor 601")
    P601: float = Field(..., description="Pump 601")
    P602: float = Field(..., description="Pump 602")
    P603: float = Field(..., description="Pump 603")


def _generate_example():
    """Generate an example sensor reading with typical normal values."""
    return {
        "FIT101": 2.0,
        "LIT101": 800.0,
        "MV101": 1.0,
        "P101": 1.0,
        "P102": 2.0,
        "AIT201": 250.0,
        "AIT202": 250.0,
        "AIT203": 250.0,
        "FIT201": 2.5,
        "MV201": 1.0,
        "P201": 1.0,
        "P202": 2.0,
        "P203": 1.0,
        "P204": 2.0,
        "P205": 1.0,
        "P206": 2.0,
        "DPIT301": 200.0,
        "FIT301": 1.5,
        "LIT301": 800.0,
        "MV301": 1.0,
        "MV302": 1.0,
        "MV303": 0.0,
        "MV304": 0.0,
        "P301": 1.0,
        "P302": 2.0,
        "AIT401": 250.0,
        "AIT402": 250.0,
        "FIT401": 1.0,
        "LIT401": 600.0,
        "P401": 1.0,
        "P402": 2.0,
        "P403": 1.0,
        "P404": 2.0,
        "UV401": 100.0,
        "AIT501": 300.0,
        "AIT502": 300.0,
        "AIT503": 300.0,
        "AIT504": 300.0,
        "FIT501": 1.2,
        "FIT502": 1.2,
        "FIT503": 1.5,
        "FIT504": 0.8,
        "P501": 1.0,
        "P502": 2.0,
        "PIT501": 150.0,
        "PIT502": 140.0,
        "PIT503": 160.0,
        "FIT601": 1.0,
        "P601": 1.0,
        "P602": 2.0,
        "P603": 1.0,
    }


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "SWaT Intrusion Detection System",
        "version": "1.0.0",
        "description": "POST sensor readings to /predict endpoint",
        "docs": "/docs",
    }


@app.post("/predict")
async def predict(reading: SensorReading):
    """
    Predict whether a sensor reading indicates Normal operation or Attack.

    Args:
        reading: SensorReading object with all 51 sensor values

    Returns:
        JSON with attack probability and classification
    """
    # Convert Pydantic model to dictionary
    sensor_dict = reading.model_dump()

    # Vectorize using DictVectorizer
    X = dv.transform([sensor_dict])

    # Get prediction probability
    prob = model.predict_proba(X)[0, 1]

    # Classify (threshold = 0.5)
    classification = "Attack" if prob >= 0.5 else "Normal"

    return {
        "attack_probability": float(prob),
        "classification": classification,
        "confidence": float(max(prob, 1 - prob)),
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "model_loaded": model is not None}
