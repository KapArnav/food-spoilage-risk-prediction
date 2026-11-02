from __future__ import annotations

import pandas as pd

from ml.data import FEATURE_COLUMNS, SOURCE_COLUMN_MAP, TARGET_COLUMN, build_preprocessor, load_provisional_dataset


def _write_fixture(path) -> None:
    rows = [
        ["Orange", 22, 95, 7.3, 361, "Good"],
        ["Orange", 22, 95, 7.3, 361, "Good"],
        ["Banana", 25, 89, 20.1, 388, "BAD"],
        ["Tomato", 25, 95, 14.6, 380, "Bad"],
    ]
    pd.DataFrame(rows, columns=SOURCE_COLUMN_MAP).to_csv(path, index=False)


def test_loading_normalizes_labels_and_removes_exact_duplicates(tmp_path) -> None:
    csv_path = tmp_path / "fixture.csv"
    _write_fixture(csv_path)
    data, profile = load_provisional_dataset(csv_path)

    assert profile.rows_read == 4
    assert profile.exact_duplicates_removed == 1
    assert len(data) == 3
    assert sorted(data[TARGET_COLUMN].tolist()) == [0, 1, 1]
    assert list(data.columns) == FEATURE_COLUMNS + [TARGET_COLUMN]


def test_preprocessor_handles_unseen_fruit_without_changing_shape(tmp_path) -> None:
    csv_path = tmp_path / "fixture.csv"
    _write_fixture(csv_path)
    data, _ = load_provisional_dataset(csv_path)
    preprocessor = build_preprocessor().fit(data[FEATURE_COLUMNS])
    transformed = preprocessor.transform(pd.DataFrame([{
        "fruit": "Mango", "temp_c": 24, "humidity_pct": 90, "light_lux": 11, "co2_ppm": 300,
    }]))
    assert transformed.shape[0] == 1
    assert transformed.shape[1] == preprocessor.transform(data[FEATURE_COLUMNS]).shape[1]
