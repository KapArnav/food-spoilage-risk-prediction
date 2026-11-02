# Model Architecture

## Status: implemented baseline

The Phase 2 model is a tabular binary MLP:

1. Eight preprocessed inputs: four standardized numeric features and four one-hot fruit indicators.
2. Dense layer with 32 ReLU units.
3. Dropout with rate 0.20.
4. Dense layer with 16 ReLU units.
5. One sigmoid output for `P(Bad storage-condition label)`.

It uses Adam (learning rate 0.001), binary cross-entropy, batch size 32, and up to 50 epochs with validation-loss early stopping. This differs from the deck's softmax diagram because the verified target is binary.
