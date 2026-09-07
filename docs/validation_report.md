# Validation Report

Checked `data/raw/prices.csv` (1010 rows) against 6 rules.

| Rule | Rows Failed (profiler, independent) | Rows Rejected (during sequential cleaning) | Action Taken |
|---|---|---|---|
| Positive price | 53 | 53 | Rejected |
| Duplicate IDs | 54 | 32 | Rejected |
| Duplicate rows | 20 | 20 | Rejected (kept first occurrence) |
| Valid date | 30 | 26 | Rejected |
| Missing market | 194 | 171 | Imputed with "Unknown" |
| Inconsistent commodity casing  | 503| (fixed via normalise)|  Normalised  |
| Unknown commodity | 0 | 0 | None found |

Note: profiler counts are computed independently on the raw file; cleaning
counts are lower for some rules because earlier rejections (e.g. duplicate
rows) remove rows before later rules are evaluated, so the same row cannot
be double-counted across rules during cleaning.

## Raw File Integrity
SHA-256 hash of `data/raw/prices.csv` was identical before and after running
the full profiling + cleaning pipeline, confirming the raw file was never
modified:
`626463245639956fc41c84cca6405bd5c6e144cdf3f976574770bbfd6a83a073`