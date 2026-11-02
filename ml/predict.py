"""Command-line prediction using saved Phase 2 artifacts."""

from __future__ import annotations

import argparse
import json

from ml.inference import StorageInputs, load_bundle, predict_storage_condition


def main() -> None:
    parser = argparse.ArgumentParser(description="Predict a Good/Bad storage-condition label.")
    parser.add_argument("--artifacts-dir", default="models/provisional_mlp")
    parser.add_argument("--fruit", required=True)
    parser.add_argument("--temp", type=float, required=True, help="Temperature in degrees Celsius")
    parser.add_argument("--humidity", type=float, required=True, help="Relative humidity percent")
    parser.add_argument("--light", type=float, required=True, help="Light intensity in documented Lux units")
    parser.add_argument("--co2", type=float, required=True, help="CO2 concentration in documented ppm units")
    args = parser.parse_args()
    bundle = load_bundle(args.artifacts_dir)
    prediction = predict_storage_condition(
        bundle,
        StorageInputs(args.fruit, args.temp, args.humidity, args.light, args.co2),
    )
    print(json.dumps(prediction, indent=2))


if __name__ == "__main__":
    main()
