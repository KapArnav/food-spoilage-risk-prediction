# ADR-004: Database design

## Status

Proposed.

## Decision

Use Supabase only for non-essential prediction history. The local inference workflow must not depend on an active database connection.

## Consequence

The backend will degrade gracefully when Supabase settings are absent or a connection fails.
