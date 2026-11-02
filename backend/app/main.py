"""Minimal FastAPI layer over the existing Phase 2 inference artifacts."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from ml.inference import PredictionBundle, StorageInputs, load_bundle, predict_storage_condition

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ARTIFACTS_DIR = PROJECT_ROOT / "models" / "provisional_mlp"


class PredictionRequest(BaseModel):
    """Validated environmental inputs used by the trained classifier."""

    fruit: Literal["Orange", "Pineapple", "Banana", "Tomato"]
    temp: float = Field(ge=-10, le=60, description="Temperature in degrees Celsius")
    humid: float = Field(ge=0, le=100, description="Relative humidity percentage")
    light: float = Field(ge=0, le=10000, description="Light intensity in Lux")
    co2: float = Field(ge=0, le=10000, description="CO2 concentration in ppm")

    @field_validator("fruit")
    @classmethod
    def normalize_fruit(cls, value: str) -> str:
        return value.strip()


class PredictionResponse(BaseModel):
    predicted_class: Literal["Good", "Bad"]
    probability_bad: float
    probability_good: float
    interpretation: str


def artifacts_dir() -> Path:
    """Return a configurable local artifacts directory."""

    return Path(os.getenv("MODEL_ARTIFACTS_DIR", str(DEFAULT_ARTIFACTS_DIR)))


@lru_cache(maxsize=1)
def get_bundle() -> PredictionBundle:
    """Load the existing model and preprocessor once per process."""

    return load_bundle(artifacts_dir())


def get_metadata() -> dict[str, object]:
    return get_bundle().metadata


app = FastAPI(
    title="Food Spoilage Risk Prediction Demo API",
    version="0.1.0",
    description="Local API for binary storage-condition classification.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/model-info")
def model_info() -> dict[str, object]:
    """Expose only measured metadata from the saved Phase 2 run."""

    try:
        metadata = get_metadata()
    except (FileNotFoundError, OSError, ValueError) as exc:
        raise HTTPException(status_code=503, detail=f"Model artifacts are unavailable: {exc}") from exc
    return {
        "model_type": "TensorFlow/Keras feed-forward neural network",
        "target_label": "Good/Bad storage-condition label, with Bad as the positive class",
        "dataset_status": metadata["dataset_provenance"],
        "metrics": metadata["test_metrics"],
        "model": metadata["model"],
        "limitations": [
            "This is storage-condition classification, not future spoilage forecasting.",
            "This is not a food-safety or food-freshness assessment.",
        ],
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    """Score one validated storage-condition record using the saved pipeline."""

    try:
        prediction = predict_storage_condition(
            get_bundle(),
            StorageInputs(
                fruit=request.fruit,
                temp_c=request.temp,
                humidity_pct=request.humid,
                light_lux=request.light,
                co2_ppm=request.co2,
            ),
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        raise HTTPException(status_code=503, detail=f"Prediction service is unavailable: {exc}") from exc
    predicted = str(prediction["predicted_class"])
    interpretation = (
        "The submitted conditions align with the model's Good storage-condition label."
        if predicted == "Good"
        else "The submitted conditions align with the model's Bad storage-condition label."
    )
    return PredictionResponse(
        predicted_class=predicted,  # type: ignore[arg-type]
        probability_bad=float(prediction["probability_bad"]),
        probability_good=float(prediction["probability_good"]),
        interpretation=interpretation,
    )
