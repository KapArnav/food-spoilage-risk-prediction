# Project Overview

## Purpose

This project will evaluate whether a neural-network-based classifier can estimate spoilage-related storage-condition risk from verified tabular food-storage data and present an operator-facing recommendation.

## Review prototype boundary

The review prototype aims to demonstrate a reproducible pipeline and a local application. It does not claim certified food-safety decision-making, production deployment, or validated future-spoilage forecasting.

## Intended flow

Verified dataset → train-only preprocessing → Keras MLP → probability → documented decision policy → recommendation → optional history storage.
