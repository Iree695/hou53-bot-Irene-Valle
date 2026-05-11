import pandas as pd
from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def build_sample_payload() -> dict:
    sample = (
        pd.read_csv("data/raw/house_prices.csv", na_values="?")
        .drop(columns=["SalePrice", "Id"])
        .iloc[0]
        .to_dict()
    )
    return {key: (None if pd.isna(value) else value) for key, value in sample.items()}


def test_root_endpoint_returns_running_message():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "HOU53-bot API is running"}


def test_predict_endpoint_returns_predicted_price():
    payload = build_sample_payload()

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert "predicted_price" in body
    assert isinstance(body["predicted_price"], float)
