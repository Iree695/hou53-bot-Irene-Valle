from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

from src.api.schemas import HouseFeatures, PredictionResponse

APP_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = APP_ROOT / "models" / "house_price_model.joblib"

app = FastAPI(title="HOU53-bot API", version="0.1.0")


@lru_cache
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


@app.get("/")
def read_root():
    return {"message": "HOU53-bot API is running"}


@app.post("/predict", response_model=PredictionResponse)
def predict_price(features: HouseFeatures):
    try:
        input_df = pd.DataFrame([features.model_dump(by_alias=True)])
        prediction = load_model().predict(input_df)[0]
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Prediction failed: {exc}",
        ) from exc

    return PredictionResponse(predicted_price=float(prediction))
