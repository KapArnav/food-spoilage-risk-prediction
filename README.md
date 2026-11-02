# NNDL Food Spoilage Prediction Framework

Review prototype for a B.Tech CSE AIML project: **Development of Neural Network Based Prediction Framework for Food Spoilage Risk in Temperature Controlled Supply Chains**.

## Status

Phase 3 review demo is complete. The repository contains a local TensorFlow/Keras baseline, FastAPI inference API, and React dashboard trained on a provisional secondary dataset copy. It does not contain Supabase integration or a future-spoilage forecasting model.

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

## Review demo startup

Open two PowerShell terminals from the repository root.

```powershell
# Terminal 1: API at http://127.0.0.1:8000
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

```powershell
# Terminal 2: dashboard at http://127.0.0.1:5173
cd frontend
npm run dev
```

The dashboard calls the API at `http://127.0.0.1:8000` by default. Set `VITE_API_BASE_URL` before running Vite only when using another API address.

## Review-demo workflow

1. Start the API and dashboard.
2. Open `http://127.0.0.1:5173`.
3. Confirm the model-performance section has loaded.
4. Use the prefilled Orange example or enter one of the supported fruit types and environmental readings.
5. Select **Predict storage condition**.
6. Explain that the result is the neural network's Good/Bad storage-condition label and probability, not a food-safety decision or future-spoilage forecast.
