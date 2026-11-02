# API Documentation

## Local startup

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

The API uses `models/provisional_mlp/` by default. Set `MODEL_ARTIFACTS_DIR` to override that local artifact location.

## Endpoints

### `GET /health`

Returns `{ "status": "ok" }` when the application process is available.

### `GET /model-info`

Returns the Keras MLP description, binary target semantics, saved test metrics, dataset-provenance caveat, and scope limitations. The metrics come from the saved Phase 2 metadata and are not recomputed by this endpoint.

### `POST /predict`

Classifies one current storage-condition record with the existing saved preprocessing pipeline and Keras model.

```json
{
  "fruit": "Orange",
  "temp": 22,
  "humid": 95,
  "light": 7.358649263,
  "co2": 361
}
```

`fruit` must be Orange, Pineapple, Banana, or Tomato. The API validates numeric types and reasonable broad ranges before calling the model. Invalid inputs return FastAPI's HTTP 422 validation response. Missing artifacts return HTTP 503.

The response includes `predicted_class`, `probability_bad`, `probability_good`, and a plain-language interpretation. It does not return a future-spoilage forecast, food-safety decision, or learned multi-band risk class.
