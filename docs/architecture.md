# Architecture

## Proposed components

- **ML pipeline**: data inspection, train-only preprocessing, Keras MLP training, evaluation, artifacts.
- **Inference service**: FastAPI validation, artifact loading, probability output, CSV handling.
- **Decision policy**: configurable probability thresholds and condition-aware recommendations.
- **Frontend**: React pages for dashboard, manual prediction, results, batch analysis, analytics, history, and model insights.
- **Persistence**: optional Supabase prediction history.

The neural network supplies model output. The decision policy translates that output and stated context into a recommendation.
