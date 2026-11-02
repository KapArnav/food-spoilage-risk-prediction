# NNDL Food Spoilage Prediction Framework

Review prototype for a B.Tech CSE AIML project: **Development of Neural Network Based Prediction Framework for Food Spoilage Risk in Temperature Controlled Supply Chains**.

## Status

Phase 0 is complete. The repository contains project governance and research documentation only. It does not yet contain a dataset, trained model, backend, frontend, or verified performance results.

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

Phase 1 will locate and inspect the public dataset before any preprocessing or model training begins.
