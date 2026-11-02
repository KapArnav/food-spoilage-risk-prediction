# ADR-003: Neural-network architecture

## Status

Proposed, pending dataset verification.

## Decision

Start evaluation with an MLP, using the deck's 64 → 32 → dropout → 16 dense-layer concept only if it suits the verified input and target structure.

## Consequence

Output activation, loss, class handling, and final layer sizes will follow verified labels rather than presentation assumptions.
