# ADR-001: Technology stack

## Status

Accepted for the review prototype.

## Decision

Use React/TypeScript/Vite for the frontend, FastAPI/Pydantic for the backend, TensorFlow/Keras for the neural network, and optional Supabase PostgreSQL for prediction history.

## Rationale

This matches the supplied project scope and keeps a clear separation between interface, inference, model training, and persistence.
