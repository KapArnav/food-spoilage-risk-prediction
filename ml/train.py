"""Train and evaluate a minimal Keras MLP for the provisional dataset."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import joblib
import numpy as np
import tensorflow as tf
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split

from ml.data import FEATURE_COLUMNS, TARGET_COLUMN, build_preprocessor, load_provisional_dataset

SEED = 42


def set_reproducibility_seed() -> None:
    random.seed(SEED)
    np.random.seed(SEED)
    tf.keras.utils.set_random_seed(SEED)


def build_model(input_features: int) -> tf.keras.Model:
    """Build a small explainable binary MLP for tabular data."""

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(input_features,), name="storage_features"),
        tf.keras.layers.Dense(32, activation="relu", name="dense_32"),
        tf.keras.layers.Dropout(0.20, name="dropout"),
        tf.keras.layers.Dense(16, activation="relu", name="dense_16"),
        tf.keras.layers.Dense(1, activation="sigmoid", name="bad_probability"),
    ], name="food_condition_mlp")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss="binary_crossentropy",
        metrics=[
            tf.keras.metrics.BinaryAccuracy(name="accuracy"),
            tf.keras.metrics.Precision(name="precision"),
            tf.keras.metrics.Recall(name="recall"),
            tf.keras.metrics.AUC(name="roc_auc"),
        ],
    )
    return model


def metric_report(y_true: np.ndarray, probabilities: np.ndarray) -> dict[str, object]:
    """Calculate held-out binary metrics from probabilities without fabrication."""

    predicted = (probabilities >= 0.5).astype(int)
    return {
        "accuracy": float(accuracy_score(y_true, predicted)),
        "precision_bad": float(precision_score(y_true, predicted, zero_division=0)),
        "recall_bad": float(recall_score(y_true, predicted, zero_division=0)),
        "f1_bad": float(f1_score(y_true, predicted, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_true, probabilities)),
        "confusion_matrix_labels": ["Good", "Bad"],
        "confusion_matrix": confusion_matrix(y_true, predicted, labels=[0, 1]).tolist(),
    }


def train(dataset_path: str | Path, artifacts_dir: str | Path, epochs: int = 50) -> dict[str, object]:
    """Train once and save paired artifacts plus evaluated held-out metrics."""

    set_reproducibility_seed()
    dataset, profile = load_provisional_dataset(dataset_path)
    features = dataset[FEATURE_COLUMNS]
    labels = dataset[TARGET_COLUMN].to_numpy()

    x_train_val, x_test, y_train_val, y_test = train_test_split(
        features, labels, test_size=0.20, stratify=labels, random_state=SEED,
    )
    x_train, x_validation, y_train, y_validation = train_test_split(
        x_train_val, y_train_val, test_size=0.20, stratify=y_train_val, random_state=SEED,
    )

    preprocessor = build_preprocessor()
    x_train_processed = preprocessor.fit_transform(x_train)
    x_validation_processed = preprocessor.transform(x_validation)
    x_test_processed = preprocessor.transform(x_test)

    model = build_model(x_train_processed.shape[1])
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss", patience=8, restore_best_weights=True,
        )
    ]
    history = model.fit(
        x_train_processed,
        y_train,
        validation_data=(x_validation_processed, y_validation),
        epochs=epochs,
        batch_size=32,
        verbose=0,
        callbacks=callbacks,
    )
    probabilities = model.predict(x_test_processed, verbose=0).reshape(-1)
    metrics = metric_report(y_test, probabilities)

    artifact_path = Path(artifacts_dir)
    artifact_path.mkdir(parents=True, exist_ok=True)
    model.save(artifact_path / "food_condition_mlp.keras")
    joblib.dump(preprocessor, artifact_path / "preprocessor.joblib")
    results: dict[str, object] = {
        "dataset_provenance": "provisional secondary copy; not the original verified Mendeley file",
        "dataset_profile": {
            "source_path": profile.source_path,
            "rows_read": profile.rows_read,
            "exact_duplicates_removed": profile.exact_duplicates_removed,
            "rows_after_deduplication": profile.rows_after_deduplication,
            "class_counts_after_deduplication": profile.class_counts,
        },
        "split_rows": {
            "train": int(len(y_train)),
            "validation": int(len(y_validation)),
            "test": int(len(y_test)),
        },
        "model": {
            "input_features": int(x_train_processed.shape[1]),
            "layers": ["Dense(32, relu)", "Dropout(0.20)", "Dense(16, relu)", "Dense(1, sigmoid)"],
            "epochs_requested": epochs,
            "epochs_completed": len(history.history["loss"]),
        },
        "test_metrics": metrics,
    }
    (artifact_path / "model_metadata.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8",
    )
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the provisional food-condition MLP.")
    parser.add_argument("--dataset", required=True, help="Path to the provisional CSV file")
    parser.add_argument("--artifacts-dir", default="models/provisional_mlp", help="Directory for generated artifacts")
    parser.add_argument("--epochs", type=int, default=50, help="Maximum training epochs")
    args = parser.parse_args()
    results = train(args.dataset, args.artifacts_dir, epochs=args.epochs)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
