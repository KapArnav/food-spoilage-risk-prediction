# Methodology

## Planned, pending dataset verification

1. Inspect and document the public dataset.
2. Define a leakage-safe train, validation, and test split.
3. Fit missing-value handling, encoding, scaling, and feature engineering only on training data.
4. Train a Keras MLP appropriate for the verified label structure.
5. Evaluate only with metrics supported by the labels.
6. Save model and preprocessing artifacts together for inference.
7. Apply a separate, documented policy to generate risk bands and recommendations.

The deck's future-escalation language will remain a research goal unless the data supports temporal forecasting.
