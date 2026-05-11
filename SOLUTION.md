# SOLUTION

## Project overview

This project delivers an end-to-end house price prediction system based on the Ames Housing dataset. The solution includes exploratory data analysis, a reusable preprocessing and training workflow, a prediction API built with FastAPI, a lightweight frontend for natural-language interaction, and a Docker Compose setup to run the application as an integrated system.

The application allows a user to describe a house in natural language, extracts a subset of meaningful features from that text, and returns a predicted sale price.

## Repository structure

- `notebooks/01_EDA.ipynb`: exploratory data analysis.
- `notebooks/02_MODEL.ipynb`: modeling workflow, model comparison, and model export.
- `src/pipeline.py`: reusable preprocessing utilities shared between training and inference.
- `src/api/`: FastAPI application, schemas, and natural-language parser.
- `frontend/`: static frontend files for the user interface.
- `models/house_price_model.joblib`: trained model artifact used by the API.
- `tests/test_api.py`: smoke tests for the API.
- `docker-compose.yml`: orchestration for backend and frontend services.

## How to run the project

### 1. Local execution

Sync dependencies:

```bash
uv sync
```

Run the backend API:

```bash
.\.venv\Scripts\python.exe -m uvicorn src.api.main:app --reload
```

The API will be available at:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`

Run the frontend in a second terminal:

```bash
.\.venv\Scripts\python.exe -m http.server 8080 -d frontend
```

The frontend will be available at:

- `http://127.0.0.1:8080`

### 2. Docker execution

Make sure Docker Desktop is running, then execute:

```bash
docker compose up --build
```

Services:

- Frontend: `http://127.0.0.1:8080`
- API: `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`

## Usage example

Example text input:

```text
A good two-story house in Gilbert with 3 bedrooms, 2 bathrooms, 1800 square feet, central air, and a 2 car garage built in 2005.
```

Expected behavior:

- the frontend sends the text to the API,
- the API extracts structured features,
- the trained model returns a predicted price,
- the frontend displays the predicted value and the detected features.

## Technical decisions

### Data analysis and modeling

- The dataset was analyzed in a dedicated EDA notebook before finalizing the training workflow.
- Training and inference were aligned through a reusable preprocessing module in `src/pipeline.py`.
- The preprocessing flow includes:
  - missing value handling,
  - automatic numeric/categorical feature detection,
  - optional numeric scaling,
  - one-hot encoding for categorical variables.
- Several regression models were compared during the modeling phase, and the selected model was exported as a serialized artifact with `joblib`.

### Shared ML core

- Preprocessing logic was extracted from the notebook into Python code to avoid training/inference drift.
- This allows the same feature transformation strategy to be reused by both the model training workflow and the API.

### API design

- The backend was implemented with FastAPI.
- Two prediction flows are available:
  - `/predict`: structured input prediction,
  - `/predict-from-text`: natural-language input prediction.
- Pydantic models are used for request and response validation.
- The model is loaded lazily and cached in memory.
- CORS was enabled for local frontend access from port `8080`.

### Natural language parsing

- A lightweight rule-based parser was implemented.
- It extracts selected fields such as bedrooms, bathrooms, living area, garage capacity, build year, neighborhood, and some quality/style cues.
- This choice keeps the solution simple, explainable, and easy to run locally without external LLM dependencies.

### Frontend

- The frontend is a static interface built with HTML, CSS, and JavaScript.
- It focuses on one main flow: writing a natural-language house description and receiving a prediction.
- The extracted features are also shown to make the behavior easier to understand.

### Docker

- The backend runs in a Python-based container using `uv`.
- The frontend runs in a lightweight Nginx container serving static files.
- Docker Compose orchestrates both services together.

## Implemented components

- Exploratory data analysis notebook.
- Modeling notebook with model comparison and export.
- Reusable preprocessing pipeline.
- Serialized trained model.
- FastAPI backend with structured prediction endpoint.
- FastAPI backend with natural-language prediction endpoint.
- Static frontend connected to the API.
- API smoke tests.
- Docker configuration for backend and frontend services.

## Limitations and future improvements

- The natural-language parser is rule-based and intentionally simple. It does not cover the full dataset vocabulary.
- The frontend is functional but minimal; it could be improved with richer validation, loading states, and more polished feedback.
- The API currently focuses on local execution and Docker deployment; production hardening would require stronger logging, monitoring, and configuration management.
- Model explainability could be expanded with explicit feature-importance or SHAP-based outputs exposed in the API and UI.
- The current parser fills only a subset of dataset features from free text; a stronger NLP layer could improve prediction quality from user descriptions.

## Validation performed

- Local API smoke tests were executed successfully.
- Structured prediction and natural-language prediction were both verified.
- Frontend and API integration was validated in the browser.
- Docker Compose configuration was validated and the application was brought up successfully after Docker Desktop was running.
