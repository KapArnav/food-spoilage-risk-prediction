from __future__ import annotations

import json

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf

from ml.data import FEATURE_COLUMNS, build_preprocessor
from ml.inference import StorageInputs, load_bundle, predict_storage_condition


def test_prediction_uses_saved_model_and_preprocessor(tmp_path) -> None:
    frame = pd.DataFrame([
        {"fruit": "Orange", "temp_c": 22, "humidity_pct": 95, "light_lux": 7, "co2_ppm": 360},
        {"fruit": "Banana", "temp_c": 26, "humidity_pct": 89, "light_lux": 20, "co2_ppm": 390},
    ], columns=FEATURE_COLUMNS)
    preprocessor = build_preprocessor().fit(frame)
    joblib.dump(preprocessor, tmp_path / "preprocessor.joblib")
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(preprocessor.transform(frame).shape[1],)),
        tf.keras.layers.Dense(1, activation="sigmoid", kernel_initializer="zeros", bias_initializer="zeros"),
    ])
    model.save(tmp_path / "food_condition_mlp.keras")
    (tmp_path / "model_metadata.json").write_text(json.dumps({"test": True}), encoding="utf-8")

    prediction = predict_storage_condition(
        load_bundle(tmp_path),
        StorageInputs("Orange", 22, 95, 7, 360),
    )
    assert prediction["predicted_class"] == "Bad"
    assert np.isclose(prediction["probability_bad"], 0.5)
