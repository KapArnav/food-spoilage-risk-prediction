# ADR-006: Dataset suitability and risk semantics

## Status

Accepted for Phase 2 planning, pending original-file acquisition.

## Context

The verified Mendeley record defines a six-column, binary `Good`/`Bad` environmental-condition dataset. It has no documented timestamp, storage-duration, observation-sequence, or future-spoilage endpoint. The review deck nevertheless proposes future risk escalation and Low, Medium, High, and Critical risk categories.

## Decision

Use the dataset only as a binary baseline for current storage-condition classification. The initial neural-network output will represent the probability of the `Bad` label after label normalization. Do not train or report a multiclass risk model from this data.

If the review prototype presents risk levels, map the binary score to a configurable policy layer and label the levels as policy-derived. Do not imply that those levels are learned target classes or a forecast horizon.

## Consequences

- Deduplicate before any split to reduce exact-record leakage.
- Document original-file provenance before training.
- A future-spoilage research claim requires a separate longitudinal dataset with a defined future outcome.
