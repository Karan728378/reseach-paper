# Forensic Re-Analysis: Pilot Dataset (261 Raw vs. 250 Clean)

## 1. Provenance and Scope
- **Raw File:** `results/pilot-summary.csv` (261 entries, SHA-256: `d258e5527c99...`)
- **Clean File:** `results/pilot-summary-clean.csv` (250 entries, SHA-256: `82ae25ded848...`)
- **Design Plan:** 5 HTML variants (`v0-baseline`, `v1-jsonld`, `v2-aria`, `v3-data-attrs`, `v4-evidence-meta`) x 5 tasks (T1-T5) x 10 repetitions = 250 planned trials.

## 2. Quantitative Discrepancy & Exclusion Breakdown
- **Raw Records:** 261 rows (251 successes, 10 failures).
  - Observed Raw Success Rate: **251/261 (96.17%)** [Wilson 95% CI: 93.09%, 97.91%]
- **Clean Records:** 250 rows (249 successes, 1 failures).
  - Observed Clean Success Rate: **249/250 (99.60%)** [Wilson 95% CI: 97.77%, 99.93%]
- **Excluded Records:** 11 records were filtered out to produce the 250-row cleaned dataset.

### Audit of the 11 Excluded Records
| # | Run ID | Rep | Variant | Task | Success | Steps | Duration | Timestamp | Forensic Classification |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `d6c79dab-9be...` | 9 | v3-data-attrs | T4 | False | 9 | 24.9s | 2026-10-06T15:04:07 | Repetition 9 Failure (Excluded in post-hoc balancing) |
| 2 | `f7bfdef8-f85...` | 9 | v3-data-attrs | T5 | False | 7 | 9.4s | 2026-10-06T15:04:16 | Repetition 9 Failure (Excluded in post-hoc balancing) |
| 3 | `1b444165-b5d...` | 9 | v4-evidence-meta | T1 | False | 7 | 10.1s | 2026-10-06T15:04:27 | Repetition 9 Failure (Excluded in post-hoc balancing) |
| 4 | `39526187-476...` | 9 | v4-evidence-meta | T2 | False | 7 | 9.9s | 2026-10-06T15:04:37 | Repetition 9 Failure (Excluded in post-hoc balancing) |
| 5 | `89cc6206-458...` | 9 | v4-evidence-meta | T3 | False | 7 | 9.6s | 2026-10-06T15:04:47 | Repetition 9 Failure (Excluded in post-hoc balancing) |
| 6 | `8ca935c1-32b...` | 9 | v4-evidence-meta | T4 | False | 7 | 9.0s | 2026-10-06T15:04:56 | Repetition 9 Failure (Excluded in post-hoc balancing) |
| 7 | `74364803-11e...` | 9 | v4-evidence-meta | T5 | False | 7 | 11.6s | 2026-10-06T15:05:08 | Repetition 9 Failure (Excluded in post-hoc balancing) |
| 8 | `1e522d81-453...` | 9 | v3-data-attrs | T4 | False | 8 | 32.3s | 2026-10-06T19:10:18 | Repetition 9 Failure (Excluded in post-hoc balancing) |
| 9 | `100f72c4-a88...` | 9 | v3-data-attrs | T5 | False | 7 | 16.7s | 2026-10-06T19:10:35 | Repetition 9 Failure (Excluded in post-hoc balancing) |
| 10 | `793d0a2f-418...` | 1 | v0-baseline | T1 | True | 4 | 38.8s | 2026-10-08T05:06:08 | Repetition 1 Extra Run |
| 11 | `270b20e3-1d8...` | 1 | v4-evidence-meta | T1 | True | 4 | 32.2s | 2026-10-08T05:08:02 | Repetition 1 Extra Run |

## 3. Scientific Impact: The Post-Hoc Selection Bias
Of the 11 excluded records:
- **9 of them were FAILURES** (all occurring in Repetition 9 on 2026-10-06 between 15:04 and 19:10 UTC).
- **Only 2 were successes** (extra duplicate runs for Repetition 1 on 2026-10-08).
- Excluding these 9 failures increased the apparent success rate from **96.17% to 99.60%** (a 3.43 percentage-point inflation).
- This proves that the 250-row pilot is a post-hoc cleaned dataset that filtered failed repetition runs rather than a strictly pre-registered ITT (Intention-To-Treat) sample.
- **Methodological Rule:** This dataset must be classified strictly as an **exploratory calibration pilot** and must NEVER be pooled with confirmatory experimental runs.

## 4. Variant x Task Success Grid (Raw vs. Clean)

### Raw Dataset (261 entries):
| Variant | T1 | T2 | T3 | T4 | T5 | Total |
|---|---|---|---|---|---|---|
| v0-baseline | 11/11 | 10/10 | 10/10 | 10/10 | 10/10 | **51/51 (100.0%)** |
| v1-jsonld | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | **50/50 (100.0%)** |
| v2-aria | 10/10 | 10/10 | 9/10 | 10/10 | 10/10 | **49/50 (98.0%)** |
| v3-data-attrs | 10/10 | 10/10 | 10/10 | 10/12 | 10/12 | **50/54 (92.6%)** |
| v4-evidence-meta | 11/12 | 10/11 | 10/11 | 10/11 | 10/11 | **51/56 (91.1%)** |

### Clean Dataset (250 entries):
| Variant | T1 | T2 | T3 | T4 | T5 | Total |
|---|---|---|---|---|---|---|
| v0-baseline | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | **50/50 (100.0%)** |
| v1-jsonld | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | **50/50 (100.0%)** |
| v2-aria | 10/10 | 10/10 | 9/10 | 10/10 | 10/10 | **49/50 (98.0%)** |
| v3-data-attrs | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | **50/50 (100.0%)** |
| v4-evidence-meta | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | **50/50 (100.0%)** |