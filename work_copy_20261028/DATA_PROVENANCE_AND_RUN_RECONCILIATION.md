# Data Provenance and Experimental Run Reconciliation
**Project:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents  
**Timestamp:** 2026-10-24  
**Workspace:** `C:\testing\research_execution_20261018\`  

---

## 1. Strict Data Categorization Framework

To safeguard scientific reproducibility and eliminate any risk of data fabrication or conflation, this project enforces four strictly segregated data tiers:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             TIER 1: LIVE EXPERIMENTAL DATA                  │
│  - Repaired live smoke trials (results/live_smoke_v2/)                      │
│    * run_001_attempt_2.json (ABS / T1: completed, score 1.0)               │
│    * run_002_attempt_2.json (ARIA / T3: completed, score 1.0)              │
│    * run_003.json           (DATA-CFG / T5: completed, score 1.0)          │
│    * run_004.json           (VIS / T6: completed, score 1.0)               │
│  - Confirmatory live runs (Future authorized 72-run benchmark)              │
├─────────────────────────────────────────────────────────────────────────────┤
│                             TIER 2: HISTORICAL SMOKE EVIDENCE               │
│  - Historical pre-repair smoke runs (results/smoke_runs/run_001 - run_004)  │
│  - Historical smoke summary (results/smoke_run_summary.csv)                 │
│  - Aborted attempt 1 for Run 1 (results/live_smoke_v2/runs/run_001.json)    │
│  - Aborted attempt 1 for Run 2 (results/live_smoke_v2/runs/run_002.json)    │
├─────────────────────────────────────────────────────────────────────────────┤
│                             TIER 3: SYNTHETIC STATISTICAL BENCHMARKS        │
│  - Synthetic RCBD datasets (test_scratch_synthetic_data/out_dataset_*)     │
│  - Statistical sensitivity simulations (audit_outputs/)                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                             TIER 4: OFFLINE UNIT TEST FIXTURES              │
│  - Sentinel pipeline fixtures (fixtures/sentinel_fixture.html)              │
│  - Deterministic mocks for unit regression tests                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Dataset Inventory and Provenance Reconciliation Matrix

| Dataset / Path | Provenance Tier | Sample Size | Model / Origin | Status & Validity | Used for Primary Hypotheses? |
|---|---|---|---|---|---|
| `results/smoke_runs/run_001.json` – `run_004.json` | **Tier 2 (Historical Smoke)** | $N=4$ | `gemini-3.1-flash-lite` | **INFRASTRUCTURE ABORTED** (Historical pre-repair socket drop masked real actions). Preserved read-only. | **NO (Never)** |
| `results/smoke_run_summary.csv` | **Tier 2 (Historical Smoke)** | 4 rows | `gemini-3.1-flash-lite` | **HISTORICAL RECORD** (Preserved as evidence of pre-repair state). | **NO** |
| `results/live_smoke_v2/runs/run_001.json` | **Tier 2 (Historical Smoke)** | $N=1$ (Attempt 1) | `gemini-3.1-flash-lite` | **INFRASTRUCTURE ABORTED** (Pre-repair socket drop post-run). Preserved for provenance. | **NO** |
| `results/live_smoke_v2/runs/run_001_attempt_2.json` | **Tier 1 (Live Smoke)** | $N=1$ (Attempt 2) | `gemini-3.1-flash-lite` | **VALID SMOKE TRIAL** (ABS/T1 verified 1.0, SoundFlow Air 3 in cart). | **NO (Smoke only, not confirmatory)** |
| `results/live_smoke_v2/runs/run_002.json` | **Tier 2 (Historical Smoke)** | $N=1$ (Attempt 1) | `gemini-3.1-flash-lite` | **INFRASTRUCTURE ABORTED** (503 Service Unavailable capacity spike). Preserved for provenance. | **NO** |
| `results/live_smoke_v2/runs/run_002_attempt_2.json` | **Tier 1 (Live Smoke)** | $N=1$ (Attempt 2) | `gemini-3.1-flash-lite` | **VALID SMOKE TRIAL** (ARIA/T3 verified 1.0, BudPro Wireless X in cart). | **NO (Smoke only, not confirmatory)** |
| `results/live_smoke_v2/runs/run_003.json` | **Tier 1 (Live Smoke)** | $N=1$ (Attempt 1) | `gemini-3.1-flash-lite` | **VALID SMOKE TRIAL** (DATA-CFG/T5 verified 1.0, pre-cart 1, post-cart empty). | **NO (Smoke only, not confirmatory)** |
| `results/live_smoke_v2/runs/run_004.json` | **Tier 1 (Live Smoke)** | $N=1$ (Attempt 1) | `gemini-3.1-flash-lite` | **VALID SMOKE TRIAL** (VIS/T6 verified 1.0, Grounded Refusal without hallucination). | **NO (Smoke only, not confirmatory)** |
| `results/live_smoke_v2/smoke_run_summary.csv` | **Tier 1 & Tier 2 Summary** | 6 rows | `gemini-3.1-flash-lite` | **AUDITABLE LOG** (Rows 1 & 3: aborted attempts; Rows 2, 4, 5, 6: completed trials). | **NO** |
| `test_scratch_synthetic_data/out_dataset_*` | **Tier 3 (Synthetic)** | $N=72 \times K$ | Algorithmic Generator | **SYNTHETIC ENGINE BENCHMARK** (Validates CMH test, ANOVA, and odds ratios). | **NO (Explicitly synthetic)** |
| `audit_outputs/` | **Tier 3 (Synthetic)** | Multiple | Algorithmic Simulation | **SENSITIVITY BENCHMARK** (Validates power calculations and sample size formulas). | **NO** |
| `fixtures/sentinel_fixture.html` | **Tier 4 (Offline Fixture)** | Static HTML | Handcrafted test fixture | **OFFLINE INTEGRATION** (Tests stage pruning without network access). | **NO** |

---

## 3. Reconciliation with `smoke_run_summary.csv`

The 6 rows of `results/live_smoke_v2/smoke_run_summary.csv` map 1-to-1 with the detailed JSON run records:

```text
Row 1: run_index=1, attempt=1 -> status="infrastructure_aborted", reason="agent_completed", error="CDP reconnect failed..."
Row 2: run_index=1, attempt=2 -> status="completed", reason="agent_completed", verifier=True (1.0)
Row 3: run_index=2, attempt=1 -> status="infrastructure_aborted", reason="infrastructure_aborted", error="503 UNAVAILABLE..."
Row 4: run_index=2, attempt=2 -> status="completed", reason="agent_completed", verifier=True (1.0)
Row 5: run_index=3, attempt=1 -> status="completed", reason="agent_completed", verifier=True (1.0)
Row 6: run_index=4, attempt=1 -> status="completed", reason="agent_completed", verifier=True (1.0)
```

### Complete Delivery Rule Audit for DATA-CFG (Row 5)
- **Serialized Attributes Found:** `data-action=True`, `data-product-id=True`.
- **Serialized Attributes Pruned:** `data-amount=False`, `data-rating=False`.
- **Verdict:** `complete_delivery=True` because both action semantics and product/entity identification were delivered in the serialized observation.

---

## 4. Preservation Policies & Integrity Commitments

1. **Zero Overwriting of Failed Attempts:** Historical smoke attempts `run_001.json` through `run_004.json` in `results/smoke_runs/` remain untouched. In `results/live_smoke_v2/`, aborted attempts for Run 1 and Run 2 were retained with exact timestamps and error traces.
2. **Elimination of Survivorship Bias:** `get_completed_run_indices()` strictly filters on `status == "completed"`. Failed or aborted attempts are never treated as completed runs.
3. **No Synthetic Conflation:** Synthetic statistical datasets are explicitly designated as statistical engine verification tests. Under no circumstances are synthetic numbers presented as live model results.
4. **Smoke vs Confirmatory Separation:** The completed 4-run smoke benchmark is certified as an engineering validation of harness functionality; it does not constitute proof of the research hypothesis.

---

## 5. Confirmatory Benchmark Reconciliation (Runs 1–41)

- **Schedule File:** [proposed_3arm_schedule.csv](file:///C:/testing/research_execution_20261018/proposed_3arm_schedule.csv) ($N=72$)
- **Canonical Summary:** [results/v3_3arm_summary.csv](file:///C:/testing/research_execution_20261018/results/v3_3arm_summary.csv) (44 rows: 3 infrastructure aborts from Run 26, 41 unique completed trials)
- **Raw Telemetry Backup:** `results/v3_3arm_summary_raw.csv` (46 rows: preserves all raw appended attempts including redundant dispatches)
- **Detail Trace Logs:** `results/3arm_runs/run_001.json` through `run_041.json` (41 verified JSON trace files)
- **Execution Progress:**
  - Block 1 (Runs 1–18): 18/18 completed (100%)
  - Block 2 (Runs 19–36): 18/18 completed (100%)
  - Block 3 (Runs 37–54): 5/18 completed (Runs 37–41)
  - Block 4 (Runs 55–72): 0/18 completed
- **Deduplication Audit:** When concurrent runner invocations appended duplicate completion lines for Runs 34 and 38, `results/v3_3arm_summary_raw.csv` was created to retain the full unaltered audit trail. The primary summary `v3_3arm_summary.csv` was deduplicated to retain the canonical first completed trial matching the on-disk JSON execution trace.
- **Trial Outcome Summary:**
  - 41/41 completed runs achieved `score=1.0` (100% verifier accuracy).
  - 3 infrastructure aborts (Run 26 attempts 1, 2, 3 due to Google Gemini 503 capacity spikes) correctly categorized and preserved without masking task success.

