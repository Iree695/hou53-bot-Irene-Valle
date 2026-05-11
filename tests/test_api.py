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


def test_predict_from_text_endpoint_returns_prediction_and_features():
    payload = {
        "description": (
            "A good two-story house in Gilbert with 3 bedrooms, 2 bathrooms, "
            "1800 square feet, central air, and a 2 car garage built in 2005."
        )
    }

    response = client.post("/predict-from-text", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert "predicted_price" in body
    assert isinstance(body["predicted_price"], float)
    assert body["extracted_features"]["BedroomAbvGr"] == 3
    assert body["extracted_features"]["FullBath"] == 2
    assert body["extracted_features"]["Neighborhood"] == "Gilbert"
