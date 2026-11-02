"""Dataset loading and leakage-safe preprocessing helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

FEATURE_COLUMNS = ["fruit", "temp_c", "humidity_pct", "light_lux", "co2_ppm"]
NUMERIC_COLUMNS = ["temp_c", "humidity_pct", "light_lux", "co2_ppm"]
CATEGORICAL_COLUMNS = ["fruit"]
TARGET_COLUMN = "bad_label"

SOURCE_COLUMN_MAP = {
    "Fruit": "fruit",
    "Temp": "temp_c",
    "Humid (%)": "humidity_pct",
    "Light (Fux)": "light_lux",
    "CO2 (pmm)": "co2_ppm",
    "Class": "source_class",
}


@dataclass(frozen=True)
class DatasetProfile:
    """Counts produced while validating one provisional input CSV."""

    source_path: str
    rows_read: int
    exact_duplicates_removed: int
    rows_after_deduplication: int
    class_counts: dict[str, int]


def load_provisional_dataset(path: str | Path) -> tuple[pd.DataFrame, DatasetProfile]:
    """Load, validate, normalize, and deduplicate the provisional CSV.

    The learned target is the source label's current Good/Bad storage-condition
    class, where 1 represents Bad. This function does not infer food safety,
    freshness, or a future spoilage outcome.
    """

    source_path = Path(path)
    if not source_path.is_file():
        raise FileNotFoundError(f"Dataset file was not found: {source_path}")

    raw = pd.read_csv(source_path)
    missing_columns = sorted(set(SOURCE_COLUMN_MAP).difference(raw.columns))
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {missing_columns}")

    rows_read = len(raw)
    deduplicated = raw.drop_duplicates().copy()
    duplicates_removed = rows_read - len(deduplicated)

    normalized = deduplicated.rename(columns=SOURCE_COLUMN_MAP).copy()
    normalized["source_class"] = (
        normalized["source_class"].astype(str).str.strip().str.casefold()
    )
    label_map = {"good": 0, "bad": 1}
    unknown_labels = sorted(set(normalized["source_class"]).difference(label_map))
    if unknown_labels:
        raise ValueError(f"Unexpected source labels: {unknown_labels}")
    normalized[TARGET_COLUMN] = normalized["source_class"].map(label_map).astype(int)

    normalized["fruit"] = normalized["fruit"].astype(str).str.strip()
    for column in NUMERIC_COLUMNS:
        normalized[column] = pd.to_numeric(normalized[column], errors="raise")

    if normalized[FEATURE_COLUMNS + [TARGET_COLUMN]].isna().any().any():
        raise ValueError("Dataset contains missing values after normalization")

    class_counts = {
        label: int(count)
        for label, count in normalized["source_class"].value_counts().sort_index().items()
    }
    profile = DatasetProfile(
        source_path=str(source_path.resolve()),
        rows_read=rows_read,
        exact_duplicates_removed=duplicates_removed,
        rows_after_deduplication=len(normalized),
        class_counts=class_counts,
    )
    return normalized[FEATURE_COLUMNS + [TARGET_COLUMN]].copy(), profile


def build_preprocessor() -> ColumnTransformer:
    """Create an unfitted transformer; fit it only with training features."""

    return ColumnTransformer(
        transformers=[
            ("numeric", StandardScaler(), NUMERIC_COLUMNS),
            ("fruit", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_COLUMNS),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )
