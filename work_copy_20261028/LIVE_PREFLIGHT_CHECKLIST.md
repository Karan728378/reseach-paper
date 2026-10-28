# LIVE RUN PREFLIGHT CHECKLIST (PROTOCOL V4)

**Document Date:** October 22, 2026  
**Auditor:** Senior Research Systems & Methodological Integrity Auditor  
**Workspace:** [`C:/testing/research_execution_20261018/`](file:///C:/testing/research_execution_20261018/)  
**Environment:** `C:\testing\.venv311\Scripts\python.exe`  
**Target Runner:** [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py)  
**Overall Preflight Status:** **PREFLIGHT READY — LIVE RUN LOCKED (GATE D: NO-GO UNTIL AUTHORIZED)**

---

## 1. Preflight Audit Checklist (14 Critical Controls)

| Item # | Preflight Control Item | Status | Verified File & Line Reference | Verification Evidence & Exact Behavior |
|:---:|---|:---:|---|---|
| **01** | **API Provider & Model IDs** | **VERIFIED** | `runner/agent-runner.py:204-205` / `protocol_v4_config.json:34` | Provider: `google`; Model: `gemini-flash-lite-latest` (fixed across pilot and confirmatory trials). |
| **02** | **Credential Management & Zero Secret Leakage** | **VERIFIED** | `protocol_v3_runner.py:62-70` | `sanitize_secret_leakage()` redacts exact key, Google AIza patterns, and Bearer tokens before disk logging. Checked securely without printing. |
| **03** | **Observation Pipeline & Treatment Delivery** | **VERIFIED** | `verify_treatment_delivery_e2e.py` / `test_agent_prompt_pipeline.py` | JSON-LD pruned (100%), interactive ARIA delivered (100%), `data-*` delivered via extended whitelist (100%). |
| **04** | **Reproducible & Privacy-Safe Logging** | **VERIFIED** | `protocol_v3_runner.py:163-176` | Full audit fields logged to `v3_run_summary.csv`. Observation previews sanitized; zero PII or credentials recorded. |
| **05** | **Single-Shot Execution (No Survivorship Retries)** | **VERIFIED** | `protocol_v3_runner.py:144-161, 270-275` | Both `success=True` and `success=False` runs count as COMPLETED and are never re-attempted. Retries-until-success strictly eliminated. |
| **06** | **Exception, Timeout & Refusal Handling** | **VERIFIED** | `protocol_v3_runner.py:180-230` | Infrastructure exceptions or timeouts record `status="failed"`, `success=False`, `score=0.0`. Refusals evaluated strictly by rubric. |
| **07** | **Primary Endpoints Pre-Specification** | **VERIFIED** | `protocol_v3_runner.py:72-135` / `task_specifications.json` | Binary scoring ($Y \in \{0, 1\}$) on client DOM state (`window.__cart__`, `window.__orderConfirmed__`). No partial credit. |
| **08** | **Orthogonal Randomization & Run Order** | **VERIFIED** | `proposed_randomized_schedule.csv` | Pre-generated RCBD schedule (seed 42, 4 blocks $\times$ 24 runs = 96 runs; 4 runs/cell). Eliminates temporal and treatment confounding. |
| **09** | **Audit Trail & Provenance Metadata** | **VERIFIED** | `protocol_v3_runner.py:164-169` | Records: `run_index`, `block_id`, `within_block_order`, `arm`, `task_id`, `variant_mapping`, `target_entity`, `success`, `score`, `total_steps`, `total_time_seconds`, `status`, `error_message`, `timestamp_end`. |
| **10** | **Run Immutability (No Silent Deletions)** | **VERIFIED** | `protocol_v3_runner.py:171` | CSV write mode is strict append (`"a"`). Existing rows are never truncated, overwritten, or omitted. |
| **11** | **Strict Maximum Runs & Spending Cap** | **VERIFIED** | `protocol_v3_runner.py:276-278` / `protocol_v4_config.json:8` | `--max-runs` parameter strictly enforced. Hard budget ceiling set at $\$10.00$ ($N=96$ pilot cost estimated at $\$0.30$–$\$0.65$). |
| **12** | **Historical Baseline Data Separation** | **VERIFIED** | `results/pilot-summary-clean.csv` | Raw historical datasets verified read-only with cryptographic SHA-256 hashes. Never mixed with post-freeze runs. |
| **13** | **Live Safety Gate at Real Entry Point** | **LOCKED** | `protocol_v3_runner.py:248-261` | Live execution unconditionally halts with `RuntimeError` unless explicit researcher sign-off is granted. Tested and verified. |
| **14** | **Launch Command Preflight Tested** | **VERIFIED** | `offline_test_suite.py` / `run_offline_pipeline_demo.py` | Complete pipeline, CLI flags, schedule consumption, and analysis verified end-to-end with zero paid API expenditure ($0.00 spent). |

---

## 2. API Key and Environment Status

* **`GOOGLE_API_KEY` Status in Current Terminal:** **NOT SET** (Environment variable is absent or empty).
* **Security Check:** Verified that no API keys are hardcoded in source files or tracked in git.
* **Pre-requisite for Live Run:** Prior to launching live trials, the researcher must export the key in the local terminal session:
  ```powershell
  $env:GOOGLE_API_KEY = "AIzaSy..."
  ```
  *(Never commit or paste the key into files or public prompts).*

---

## 3. Cost & Resource Projections

Based on actual token measurement in [`test_agent_prompt_pipeline.py`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py):
* **Average prompt size:** ~26,900 characters (~6,725 tokens) per step.
* **Average steps per task:** ~4 steps.
* **Tokens per run:** ~27,000 input tokens, ~300 output tokens.
* **Pricing (`gemini-flash-lite-latest`):** $\$0.075$ per 1M input tokens, $\$0.30$ per 1M output tokens.
* **Cost per run:** $\approx \$0.0022$–$\$0.0035$.

| Study Configuration | Total Runs ($N$) | Primary Tasks ($N_{\text{prim}}$) | Estimated Run Time | Estimated Cost (USD) | Spending Ceiling (USD) |
|---|:---:|:---:|:---:|:---:|:---:|
| **Exploratory Pilot** | 96 | 80 | ~45 minutes | **$\$0.30 – \$0.65$** | $\$10.00$ |
| **Confirmatory Superiority Trial** | 480 | 400 | ~3.5 hours | **$\$1.50 – \$3.25$** | $\$15.00$ |

---

## 4. Preflight Conclusion

The experimental harness, runner, verifiers, logging, schedule, and safety controls have passed all 14 preflight checkpoints. The active runner is **100% prepared for live execution**, but remains **strictly gated** until explicit researcher authorization is granted.
