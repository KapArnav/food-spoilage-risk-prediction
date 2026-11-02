# Evaluation Results

## EXP-001 held-out test set

| Metric | Value |
| --- | ---: |
| Accuracy | 0.9926 |
| Precision for Bad | 0.9986 |
| Recall for Bad | 0.9845 |
| F1 for Bad | 0.9915 |
| ROC-AUC | 0.9989 |

Confusion matrix with rows as actual `[Good, Bad]` and columns as predicted `[Good, Bad]`:

```text
[[913, 1],
 [ 11, 698]]
```

These values are measured on the 1,623-row held-out split after exact-row deduplication. They are not evidence of future-spoilage forecasting, food-safety prediction, or real-world performance. The provisional source and duplicate-heavy original input may make them optimistic.
