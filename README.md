# NNDL Food Spoilage Prediction Framework

Review prototype for a B.Tech CSE AIML project: **Development of Neural Network Based Prediction Framework for Food Spoilage Risk in Temperature Controlled Supply Chains**.

## Status

Phase 2 is complete. The repository contains a local TensorFlow/Keras baseline and command-line prediction pipeline trained on a provisional secondary dataset copy. It does not contain a backend, frontend, Supabase integration, or a future-spoilage forecasting model.

## Planned prototype

- Neural-network inference from verified storage-condition features.
- Manual and CSV batch prediction.
- A documented policy that maps model probability to risk bands and recommendations.
- Optional Supabase prediction history.
- React research dashboard and FastAPI API.

## Important research note

The original review deck describes a binary Good/Bad storage-condition target and also describes Low, Medium, High, and Critical risk categories. Until a dataset is verified, the latter must be treated as configurable decision-policy bands, not learned multiclass labels.

## Documentation

Read [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) for the current persistent project state. Supporting records are in [docs](docs/).

## Next approved phase

The current model predicts the dataset's binary Good/Bad storage-condition label only. See [dataset documentation](docs/dataset_documentation.md) and [evaluation results](docs/experiments/evaluation_results.md) before using it in a review demonstration.

## Local Phase 2 commands

The local CSV and model artifacts are intentionally ignored by Git. Set a dataset path explicitly.

```powershell
.\.venv\Scripts\python.exe -m ml.train --dataset data\raw\fruit_spoilage_secondary.csv --artifacts-dir models\provisional_mlp
.\.venv\Scripts\python.exe -m ml.predict --artifacts-dir models\provisional_mlp --fruit Orange --temp 22 --humidity 95 --light 7.36 --co2 361
.\.venv\Scripts\python.exe -m pytest -q
```
