"""Load saved artifacts and score one storage-condition record."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
import tensorflow as tf

from ml.data import FEATURE_COLUMNS


@dataclass(frozen=True)
class StorageInputs:
    fruit: str
    temp_c: float
    humidity_pct: float
    light_lux: float
    co2_ppm: float

    def as_frame(self) -> pd.DataFrame:
        if not self.fruit.strip():
            raise ValueError("fruit must not be empty")
        return pd.DataFrame([
            {
                "fruit": self.fruit.strip(),
                "temp_c": float(self.temp_c),
                "humidity_pct": float(self.humidity_pct),
                "light_lux": float(self.light_lux),
                "co2_ppm": float(self.co2_ppm),
            }
        ], columns=FEATURE_COLUMNS)


@dataclass
class PredictionBundle:
    model: tf.keras.Model
    preprocessor: Any
    metadata: dict[str, Any]


def load_bundle(artifacts_dir: str | Path) -> PredictionBundle:
    """Load paired Keras and preprocessing artifacts from one directory."""

    artifacts_path = Path(artifacts_dir)
    model_path = artifacts_path / "food_condition_mlp.keras"
    preprocessor_path = artifacts_path / "preprocessor.joblib"
    metadata_path = artifacts_path / "model_metadata.json"
    missing = [str(path) for path in (model_path, preprocessor_path, metadata_path) if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing model artifact files: {missing}")
    return PredictionBundle(
        model=tf.keras.models.load_model(model_path),
        preprocessor=joblib.load(preprocessor_path),
        metadata=json.loads(metadata_path.read_text(encoding="utf-8")),
    )


def predict_storage_condition(bundle: PredictionBundle, inputs: StorageInputs) -> dict[str, float | str]:
    """Return the learned current storage-condition class and Bad probability."""

    transformed = bundle.preprocessor.transform(inputs.as_frame())
    probability_bad = float(bundle.model.predict(transformed, verbose=0).reshape(-1)[0])
    predicted_class = "Bad" if probability_bad >= 0.5 else "Good"
    return {
        "predicted_class": predicted_class,
        "probability_bad": probability_bad,
        "probability_good": 1.0 - probability_bad,
    }
