# Requirements

## Functional requirements

- Accept manual inputs supported by the verified model.
- Validate and process compatible CSV files in batches.
- Return the model output, a policy-derived risk band, and a separate recommendation.
- Persist history to Supabase only when configuration and connectivity are available.
- Present model and dataset information without fabricated claims.

## Non-functional requirements

- Run locally with documented commands.
- Keep preprocessing artifacts consistent between training and inference.
- Handle invalid inputs and unavailable database connectivity gracefully.
- Keep the UI minimal, light, readable, and research-oriented.
