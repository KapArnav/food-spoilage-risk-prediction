# Project Context

## Project title

Development of Neural Network Based Prediction Framework for Food Spoilage Risk in Temperature Controlled Supply Chains

## Objectives from the review proposal

The project proposes a neural-network-based framework that analyzes food or fruit type and storage-environment variables to estimate spoilage-related risk and provide an early-warning recommendation for cold-chain operators. The review deck highlights temperature, humidity, storage duration, light intensity, CO2 concentration, product type, environmental deviations, and exposure history.

## Current scope

This repository currently contains **Phase 0 only**: project inspection, durable documentation, safe Git setup, and initial architecture planning. No dataset has been downloaded, no model has been trained, and no application code has been implemented.

The intended review prototype will later include a React frontend, FastAPI backend, TensorFlow/Keras MLP, manual and CSV prediction flows, recommendation policy, optional Supabase prediction history, analytics, and model-insight views.

## Technology decisions

- Frontend: React, TypeScript, Vite, Tailwind CSS, shadcn/ui, React Router, TanStack Query, Recharts, Lucide.
- Backend: Python, FastAPI, Pydantic, Uvicorn.
- ML: TensorFlow/Keras, NumPy, pandas, scikit-learn.
- Persistence: Supabase PostgreSQL, configured through environment variables.

These are approved proposal-stack decisions. Dependency installation and project scaffolding are deferred until Phase 1 approval.

## Dataset status

The review deck names a 2025 Mendeley Data resource, "Multi-Parameter Fruit Spoilage Prediction Dataset", and states 10,996 records with fruit type, temperature, humidity, light intensity, CO2 concentration, and a Good/Bad target. These statements remain **unverified**. The project must locate and inspect the source before implementing preprocessing, labels, or training.

## Neural-network status

The proposed architecture is an MLP with Dense 64 ReLU, Dense 32 ReLU, Dropout, Dense 16 ReLU, and a softmax output in the methodology diagram. The master brief separately proposes a 64/32/Dropout initial candidate. Architecture, output activation, loss, and metrics remain pending verified target semantics.

## Research decisions and open questions

1. A binary Good/Bad target cannot directly train the Low/Medium/High or Critical risk classes shown in the deck. If the dataset is binary, the model will predict a binary probability and a separately documented decision-policy threshold will map it to risk bands.
2. The proposal refers to future deterioration and risk escalation, but the named dataset description appears cross-sectional. Temporal prediction needs verified time-indexed labels and an appropriate split strategy.
3. The literature slide includes incomplete bibliographic details, including "IEEE, 2026". Literature citations need verification before they are treated as evidence.
4. Storage duration is central to the abstract and diagrams but is not included in the dataset input-feature list on the dataset slide. Dataset inspection must resolve this.
5. The deck names High-risk recall, multi-class F1, and ROC-AUC together. Final evaluation must match the verified target and risk-policy design.

## Completed milestones

- 2026-11-02: Inspected the supplied 12-slide review deck, including its embedded novelty and methodology diagrams.
- 2026-11-02: Confirmed Git is installed and the working directory is an empty existing repository on branch `master` with no commits.
- 2026-11-02: Created the persistent documentation, decision records, project graph, history graph, environment template, and ignore policy.
- 2026-11-02: Renamed the initial branch to `main` and created the local root commit `chore: initialize project structure`.

## Known issues

- Public dataset source and schema are not yet verified.
- No baseline dataset, trained model, metrics, API, UI, Supabase project, or test suite exists.
- No remote repository is configured or has been contacted.

## Next step

Await approval to begin Phase 1: locate and inspect the public dataset, then document the verified schema and label semantics before any training implementation.
