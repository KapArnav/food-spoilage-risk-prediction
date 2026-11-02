# Database Schema

## Status: planned

The intended `prediction_history` table will contain only verified model inputs, output probability, predicted class, policy-derived risk level, recommendation, source, and timestamp. A migration will be created once the verified dataset determines the input schema.

Credentials belong in environment variables and never in version control.
