# Dataset Documentation

## Verification status

**Original record verified; original file download not verified locally.** The original source is [Mendeley Data version 1](https://data.mendeley.com/datasets/czz68d9fwj/1), DOI [10.17632/czz68d9fwj.1](https://doi.org/10.17632/czz68d9fwj.1), published 29 September 2025 by Nshekanabo Marius and Stanley Mugisha. Mendeley lists Soroti University and the licence as CC BY 4.0.

The official record says the CSV contains 10,996 entries and six columns. Its current public API returned HTTP 401 for unauthenticated file and archive requests on 2026-11-02, so the repository does not store or claim to have inspected an original downloaded Mendeley file.

For a provisional schema and quality check only, Phase 1 inspected a public GitHub copy that cites the Mendeley record. Its SHA-256 was `218F76F061A12B0A38C55107E5BE3B377E9EECB33F1A1840EF2B4E4618A5E5AA`. It is a secondary copy, not evidence of byte-for-byte identity with the original file.

## Official metadata

- **Title:** A Multi-Parameter Dataset for Machine Learning Based Fruit Spoilage Prediction in an IoT-Enabled Cold Storage System
- **Purpose:** classify environmental conditions as optimal or suboptimal for spoilage prevention in a controlled, IoT-enabled cold-storage setting for smallholder farmers in Uganda.
- **Licence:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode). Reuse is permitted with appropriate attribution and an indication of changes.
- **Official target definition:** `Class`, binary `Good` or `Bad`, indicating environmental conditions that are optimal or suboptimal for spoilage prevention.

## Provisional inspected CSV schema

The secondary copy has 10,995 data rows and six columns. The one-row difference from the official 10,996-entry statement may reflect a differing entry-count convention, but cannot be resolved without the original file.

| CSV field | Provisional type | Unit or meaning | Notes |
| --- | --- | --- |
| `Fruit` | categorical string | fruit type | Orange, Pineapple, Banana, Tomato |
| `Temp` | integer | °C | Official metadata calls this temperature inside the cold-storage unit |
| `Humid (%)` | integer | relative humidity (%) | Header includes its unit |
| `Light (Fux)` | floating point | documented as Lux | The inspected header uses `Fux`, likely a typo. Preserve and normalize the name only in a documented preprocessing step. |
| `CO2 (pmm)` | integer | documented as ppm | The inspected header uses `pmm`, likely a typo. Preserve and normalize the name only in a documented preprocessing step. |
| `Class` | categorical string | binary target | Values need case normalization: `Good`, `Bad`, and `BAD` appear in the secondary copy. |

## Provisional data profile

### Labels and fruit types

After case-normalizing `BAD` to `Bad`, the secondary copy contains 5,667 `Good` rows (51.54%) and 5,328 `Bad` rows (48.46%). Fruit counts are Orange 3,330, Pineapple 2,257, Banana 1,667, and Tomato 3,741.

### Completeness and quality

- No blank values appeared in the six fields of the secondary copy.
- Exact-row duplicate count: 2,880 of 10,995 rows (26.19%), leaving 8,115 unique full rows. The largest identical-row group occurs 15 times.
- Discrete-value counts: `Temp` 7, `Humid (%)` 25, `Light (Fux)` 323, and `CO2 (pmm)` 333.
- Observed ranges: Temp 21–27 °C, humidity 71–95%, light 4.22124279–268.4478082 (documented unit: Lux), and CO2 20–478 (documented unit: ppm).
- A simple univariate 1.5×IQR screen flagged 0 temperature, 2,427 humidity, 739 light, and 363 CO2 values. These flags are distributional candidates, not confirmed sensor errors. The humidity distribution is concentrated near 94–95%, so IQR alone is not an adequate deletion rule.

## Temporal suitability

Neither the official six-field schema nor the inspected secondary copy contains timestamps, storage duration, batch identifiers, repeated-observation identifiers, measured spoilage time, or a future outcome horizon. The target describes the current environmental condition's suitability for spoilage prevention.

**Conclusion:** this data can support a binary, current storage-condition or spoilage-risk classification baseline. It does not, on its documented fields alone, support a scientifically defensible claim that the model forecasts future spoilage or predicts Low → Medium → High risk escalation.

## Implications for the review prototype

1. Treat the initial model output as `P(Bad storage-condition label)` rather than certified food spoilage probability.
2. Use `Good`/`Bad` as the learned binary target after label normalization.
3. Do not create learned Low, Medium, High, or Critical output classes from this dataset.
4. If the UI needs risk bands for review, define them as configurable **decision-policy bands** on the binary model score and label them accordingly.
5. Deduplicate before splitting, then fit all preprocessing on training data only. Random splitting before deduplication would allow exact records to leak across partitions.
6. Obtain a timestamped longitudinal dataset with an explicit future spoilage or quality endpoint before implementing a forecasting claim.
