from fastapi import FastAPI
from pydantic import BaseModel
import requests
import joblib
import pandas as pd
from collections import Counter

app = FastAPI()

CAPE_API_URL = "http://127.0.0.1:8000"


class PredictionRequest(BaseModel):
    analysis_id: int


models = {
    "XGBoost": "Model/xgb_final_model.joblib",
    "Random Forest": "Model/rf_final_model.joblib",
    "Logistic Regression": "Model/lr_final_model.joblib",
}


def extract_api_frequencies(report):

    api_counts = Counter()
    behavior = report.get("behavior", {})

    for process in behavior.get("processes", []):
        for call in process.get("calls", []):

            api = call.get("api")

            if api:
                api_counts[api] += 1

    return api_counts


def run_prediction_models(api_counts):
    results = []

    for model_name, model_path in models.items():

        saved = joblib.load(model_path)

        model = saved["model"]
        features = saved["features"]

        X = pd.DataFrame(
            [[api_counts.get(feature, 0) for feature in features]],
            columns=features,
        )

        prediction = model.predict(X)[0]

        prediction_label = (
            "Ransomware" if int(prediction) == 1 else "Benign"
        )

        result = {
            "name": model_name,
            "prediction": prediction_label,
        }

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(X)[0]

            result["probability"] = {
                (
                    "Ransomware"
                    if int(class_label) == 1
                    else "Benign"
                ): float(probability)
                for class_label, probability
                in zip(model.classes_, probabilities)
            }

        results.append(result)

    return results


@app.post("/predict/")
def predict(request: PredictionRequest):

    analysis_id = request.analysis_id

    # Get CAPEv2 report
    try:
        response = requests.get(
            f"{CAPE_API_URL}/apiv2/tasks/get/report/{analysis_id}/json/",
            timeout=60,
        )

        response.raise_for_status()
        report = response.json()

    except requests.RequestException as e:

        return {
            "status": "error",
            "analysis_id": analysis_id,
            "message": "Could not retrieve CAPEv2 report.",
            "details": str(e),
        }

    api_counts = extract_api_frequencies(report)

    if not api_counts:

        return {
            "status": "no_api_calls",
            "analysis_id": analysis_id,
            "message": (
                "No API calls were found in the CAPEv2 report. "
                "ML prediction was not performed."
            ),
        }

    results = run_prediction_models(api_counts)

    return {
        "status": "success",
        "analysis_id": analysis_id,
        "api_count": sum(api_counts.values()),
        "unique_apis": len(api_counts),
        "models": results,
    }