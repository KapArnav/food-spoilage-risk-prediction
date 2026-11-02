# Methodology

## Implemented Phase 2 baseline

1. Load the provisional secondary CSV through a configurable CLI path.
2. Normalize `Good`, `Bad`, and `BAD` labels to a binary target where `Bad` is 1.
3. Remove exact duplicate rows before stratified 64%/16%/20% train, validation, and test splitting.
4. Fit one-hot fruit encoding and numeric scaling on training features only.
5. Train Dense(32, ReLU) → Dropout(0.20) → Dense(16, ReLU) → Dense(1, sigmoid).
6. Evaluate the held-out test set with accuracy, precision, recall, F1, confusion matrix, and ROC-AUC.
7. Save the paired Keras model, fitted preprocessing pipeline, and metadata together for CLI inference.

The model predicts the dataset's Good/Bad storage-condition label only. The deck's future-escalation language remains a research goal unless a longitudinal dataset supports it.
