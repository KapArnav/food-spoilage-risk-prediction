# Project Context

## Project title

Development of Neural Network Based Prediction Framework for Food Spoilage Risk in Temperature Controlled Supply Chains

## Objectives from the review proposal

The project proposes a neural-network-based framework that analyzes food or fruit type and storage-environment variables to estimate spoilage-related risk and provide an early-warning recommendation for cold-chain operators. The review deck highlights temperature, humidity, storage duration, light intensity, CO2 concentration, product type, environmental deviations, and exposure history.

## Current scope

This repository currently contains **Phases 0 through 2**: project inspection, durable documentation, dataset-source validation, and a local TensorFlow/Keras binary baseline. No backend, frontend, synthetic data, or Supabase integration has been implemented.

The intended review prototype will later include a React frontend, FastAPI backend, TensorFlow/Keras MLP, manual and CSV prediction flows, recommendation policy, optional Supabase prediction history, analytics, and model-insight views.

## Technology decisions

- Frontend: React, TypeScript, Vite, Tailwind CSS, shadcn/ui, React Router, TanStack Query, Recharts, Lucide.
- Backend: Python, FastAPI, Pydantic, Uvicorn.
- ML: TensorFlow/Keras, NumPy, pandas, scikit-learn.
- Persistence: Supabase PostgreSQL, configured through environment variables.

These are approved proposal-stack decisions. Dependency installation and project scaffolding are deferred until Phase 1 approval.

## Dataset status

The original Mendeley Data record is verified: Nshekanabo Marius and Stanley Mugisha, 2025, DOI `10.17632/czz68d9fwj.1`, CC BY 4.0. The record describes 10,996 entries, six fields, four example fruit types, environmental inputs, and a binary `Good`/`Bad` target. Original-file download was unavailable without authentication during Phase 1. A temporary secondary copy was inspected provisionally: it has 10,995 rows, 2,880 exact duplicates, and inconsistent `BAD`/`Bad` spelling. See `docs/dataset_documentation.md` and `docs/dataset_validation.md`.

## Neural-network status

Phase 2 trained a TensorFlow/Keras MLP on the provisional secondary copy after exact-row deduplication. The model uses four scaled numeric inputs and one-hot fruit type, producing eight features. Architecture: Dense(32, ReLU) → Dropout(0.20) → Dense(16, ReLU) → Dense(1, sigmoid). It predicts the binary `Bad` storage-condition label, not future spoilage, food safety, or food freshness.

The run used stratified 64%/16%/20% train/validation/test splits after deduplication: 5,193/1,299/1,623 rows. Held-out metrics are documented in `docs/experiments/evaluation_results.md`; they must remain qualified by the provisional source and duplicate-heavy data.

## Research decisions and open questions

1. A binary Good/Bad target cannot directly train the Low/Medium/High or Critical risk classes shown in the deck. The initial model must predict the binary `Bad` label; risk bands, if displayed, are separately documented decision-policy thresholds.
2. The proposed dataset has no documented timestamp, storage-duration, sequence, or future-outcome fields. It does not scientifically support future-spoilage or risk-escalation forecasting.
3. The literature slide includes incomplete bibliographic details, including "IEEE, 2026". Literature citations need verification before they are treated as evidence.
4. Storage duration is central to the abstract and diagrams but is not included in the dataset input-feature list on the dataset slide. Dataset inspection must resolve this.
5. The deck names High-risk recall, multi-class F1, and ROC-AUC together. Final evaluation must match the verified target and risk-policy design.

## Completed milestones

- 2026-11-02: Inspected the supplied 12-slide review deck, including its embedded novelty and methodology diagrams.
- 2026-11-02: Confirmed Git is installed and the working directory is an empty existing repository on branch `master` with no commits.
- 2026-11-02: Created the persistent documentation, decision records, project graph, history graph, environment template, and ignore policy.
- 2026-11-02: Renamed the initial branch to `main` and created the local root commit `chore: initialize project structure`.
- 2026-11-02: Verified the original Mendeley dataset record, inspected a temporary secondary CSV copy, and recorded its schema, quality findings, and scope limitations.
- 2026-11-02: Trained and tested the initial local binary MLP using the provisional secondary copy. Saved artifacts locally under `models/provisional_mlp/`.

## Known issues

- Original dataset-file retrieval and checksum verification remain unresolved because Mendeley's current public API required authentication.
- The local training file remains a secondary copy, not the verified original Mendeley file.
- Test performance may be optimistic because the source has extensive duplicates and the secondary-file provenance is provisional.
- No API, UI, Supabase project, or longitudinal forecasting dataset exists.
- No remote repository is configured or has been contacted.

## Next step

Await approval to begin Phase 3: implement a minimal FastAPI inference API around the saved local artifacts.
