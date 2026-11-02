# NNDL Food Spoilage Prediction Framework

## Project objective

Build an incremental, review-ready prototype for **Development of Neural Network Based Prediction Framework for Food Spoilage Risk in Temperature Controlled Supply Chains**. Preserve the original review deck's terminology and distinguish proposal claims from validated implementation results.

## Scope and architecture

- `frontend/`: React, TypeScript, Vite, Tailwind, shadcn/ui, React Router, TanStack Query, Recharts, and Lucide.
- `backend/`: FastAPI application, validation, inference, batch prediction, recommendations, and persistence integration.
- `ml/`: dataset inspection, preprocessing, training, evaluation, and reproducible inference artifacts.
- `docs/`: durable project memory, research records, decisions, experiment results, graphs, and progress.
- `database/`: Supabase SQL migrations and schema documentation.
- `tests/`: backend and frontend tests when their respective applications exist.

Keep model training separate from inference and database access. Keep the recommendation policy separate from neural-network inference. Supabase is optional at runtime: local prediction must work if its configuration is absent.

## Research constraints

- Inspect and document a real public dataset before coding preprocessing or training.
- Do not fabricate dataset schema, model metrics, experiment outcomes, or food-safety claims.
- The review deck describes a binary Good/Bad target and a future Low/Medium/High escalation goal. Treat probability-to-risk bands as a configurable decision policy unless a verified dataset supplies multiclass labels.
- Do not claim future spoilage prediction unless labels and methodology support it.
- Clearly label synthetic data and never silently mix it into the real training dataset.

## Coding standards

- Use small, descriptive, typed modules. Python functions require type hints; TypeScript must use explicit domain types.
- Validate user input, CSV columns, model artifacts, and environment configuration at boundaries.
- Keep secrets in environment variables. Never commit `.env` files or credentials.
- Prefer straightforward local development over extra services, authentication, or deployment machinery.
- Update `PROJECT_CONTEXT.md`, `CHANGELOG.md`, `docs/progress_log.md`, `docs/project_graph.mmd`, and `docs/project_history.mmd` after each meaningful milestone.

## Testing and Git

- Run focused tests after a change and record the command and result in the progress log.
- Inspect `git status` before committing. Never overwrite existing history, force-push, or push to a remote without direct user authorization.
- Use small, meaningful commits only after relevant checks pass.
- Do not delete project files without explicit permission.
