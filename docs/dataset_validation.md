# Phase 1 Dataset Validation Record

## Sources consulted

1. [Original Mendeley Data record](https://data.mendeley.com/datasets/czz68d9fwj/1), version 1, DOI [10.17632/czz68d9fwj.1](https://doi.org/10.17632/czz68d9fwj.1).
2. [Mendeley Data API documentation](https://data.mendeley.com/api/docs/) for the public dataset and file endpoints.
3. A public GitHub copy, used only for provisional CSV inspection after the original API denied unauthenticated retrieval. This is not cited as the original source and is not stored in the repository.

## Method

On 2026-11-02, the original Mendeley landing page was inspected for authorship, publication date, DOI, licence, description, record count, column names, units, and target semantics. Calls to the documented API and archive endpoint returned HTTP 401 without credentials. A temporary, public secondary copy then underwent read-only CSV checks for row count, headers, blank values, case-sensitive label counts, exact duplicates, distinct values, numeric ranges, and 1.5×IQR candidate outliers.

## Results

The official record verifies the intended source, CC BY 4.0 licence, six-column tabular design, 10,996-entry claim, four example fruit types, and binary `Good`/`Bad` target. The secondary copy corroborates the stated structure but contains 10,995 data rows, 2,880 exact duplicates, and 711 uppercase `BAD` labels. The secondary copy has no temporal, duration, or longitudinal identifiers.

## Limitations

- The original file could not be downloaded without authentication during this milestone. The file-level checksum and all row-level statistics remain provisional until the Mendeley file itself is acquired and compared.
- The official description identifies the target as environmental suitability. It does not document laboratory spoilage measurements, a prediction horizon, or an annotation procedure.
- Outlier flags are screening results only. Phase 2 must choose any treatment after inspecting distributions by fruit and class, not by blindly deleting IQR-flagged records.

## Recommendation

Proceed to Phase 2 only as a binary environmental-condition classifier baseline, contingent on obtaining the original file or recording why the inspected copy is acceptable. Do not represent its output as future spoilage forecasting. Present any multi-band risk view as a configurable decision policy, separate from the trained classifier.
