# Consolidated Research Status & Authoritative Evidence Register

**Document ID:** `CONSOLIDATED_RESEARCH_STATUS.md`  
**Workspace:** `C:\testing\research_execution_20261018\`  
**Runtime:** Python 3.11.9 (`C:\testing\.venv311\Scripts\python.exe`), `browser-use 0.13.10`  
**Date:** October 2026  
**Auditor / Roles:** Senior Research Engineer, Experimental-Design Auditor, Reproducibility Lead  
**Operating Policy:** 100% Offline Reproduction · Zero Paid API Calls · Absolute Scientific Candor  

---

## 1. Executive Research Identity & Empirical Reality

### Primary Contribution
This research is an **Observation-Pipeline Systems Measurement and Benchmark Pre-Registration Protocol**. It investigates the discrepancy between Document Object Model (DOM) markup in rendered web pages and the actual textual representation delivered to Large Language Model (LLM) browser agents through framework serializers.

### Current Empirical Status
- **Genuine Live Behavioral Trials:** **0 Completed Runs.**
- **Paid API Dispatches / Credit Spend:** **$0.00 (Zero Spend).**
- **Safety Gate:** **LOCKED** (`SAFETY_GATE_UNLOCKED = False` in `protocol_v3_runner.py`).
- **Offline Systems & Engineering Infrastructure:** **100% Verified and Reproducible.**

All claims in draft manuscripts regarding agent task performance, reasoning, or success rates are strictly pre-registered hypotheses. No behavioral findings from real models currently exist in the repository.

---

## 2. Master Resolution Matrix for Consolidated Review Weaknesses

| Weakness ID & Category | Core Scientific Flaw | Root Cause in Repository | Executed Resolution & Evidence Artifact | Current Status |
|---|---|---|---|:---:|
| **A1 / C4 — Zero Live Evidence** | Claims about agent cognition made without live trials. Process theater of 30+ reports obscuring lack of data. | Early draft manuscripts conflated mock tests with live results. Excessive audit logs. | - Live trial count audited as exactly 0.<br>- Drafts rewritten to pre-registration framing.<br>- Automated guard (`audit_claims_and_evidence.py`) enforces clean claims.<br>- Consolidated into this single document. | **RESOLVED (Framing Aligned)** |
| **A2 / B1 — Delivery Verification** | Information loss assumed from source code snippets without end-to-end tracing into model payload. | `DISABLED_ELEMENTS` snippet cited without payload boundary verification. | - Implemented `fixtures/sentinel_fixture.html` with unique markers.<br>- Implemented `trace_sentinel_pipeline.py` & `test_sentinel_pipeline.py`.<br>- Recorded empirical trace in `sentinel_stage_trace.json`.<br>- Verified model client payload boundary using `FakeListChatModel`. | **RESOLVED (Empirically Traced)** |
| **A3 / C5 — Novelty & Prior Art** | Treating a 5-line filter in `browser-use` as a novel AI cognition discovery; straw-manning literature. | Earlier drafts claimed WebArena and Mind2Web ignored DOM filtering. | - Acknowledged WebArena, Mind2Web, and BrowserGym already documented DOM verbosity and designed tree distillation.<br>- Reframed contribution as quantifying markup transmission vs. web accessibility standards.<br>- Reframed from "agent cognition failure" to "observation pipeline serialization bottleneck". | **RESOLVED (Novelty Reframed)** |
| **A4 — Treatment Isolation & `VIS` Arm** | `VIS` arm was a text-only duplicate of `BASELINE`, confounding the comparison and wasting 25% of runs. | `use_vision=False` turned `VIS` into an exact duplicate of `v0-baseline`. | - Formalized Option A Clean 3-Arm Design (`proposed_3arm_schedule.csv`, 72 runs: ABS, ARIA, DATA-CFG).<br>- Replicate arm retired from primary comparison.<br>- Deconfounded button labels (`app-core.js:440`) verified via `test_treatment_leakage_and_integrity.py`. | **RESOLVED (Option A Clean)** |
| **A5 / C3 — Task Construct Validity** | Fragile verifiers: T4 synthetic flag, T5 localStorage pre-seed, T6 regex scoring. | Tasks conflate general navigation with semantic markup utility. | - Created `TASK_CONSTRUCT_MATRIX.md` separating primary (T1–T3) from secondary (T4–T6).<br>- Implemented `test_verifier_ground_truth_battery.py` (12 known-pass/known-fail tests passing).<br>- Hardened verifier logic eliminates historical 0.25 credit and unseeded passes. | **RESOLVED (Constructs Mapped)** |
| **A6 / B2 — Causal & Statistical Rigor** | Collider bias from conditioning on delivery ($E[Y \mid Arm, D=1]$); ~10.85% power at $N=96$. | Naive conditional estimand; confusing nonsignificant pilot results with equivalence. | - Primary estimand strictly defined as Intention-to-Treat (ITT): $E[Y \mid Arm]$.<br>- Delivery rate reported as descriptive manipulation check.<br>- Statistical power audit (`reproduce_power_audit.py`) documents pilot as exploratory ($<11\%$ power) with strict prohibition on equivalence claims. | **RESOLVED (ITT Enforced)** |
| **A7 — Manuscript Claims Exceed Evidence** | Phrases like "we prove", "flaw-free verifiers", and "fundamental discovery". | Uncalibrated draft manuscripts. | - Automated `audit_claims_and_evidence.py` executed (passes with 0 violations).<br>- `RESEARCH_PAPER_DRAFT.md` and `manuscript_draft.md` corrected. | **RESOLVED (Claims Clean)** |
| **A8 / C1 / C2 — Scope & Generalization** | Generalizing from 1 synthetic toy site and 1 framework with vision disabled to "all browser agents". | Overly ambitious claims in draft titles and introductions. | - Scope strictly bounded to `browser-use 0.13.10`, text-only mode (`use_vision=False`), and synthetic e-commerce fixture.<br>- Vision-based agents and cross-framework generalization explicitly demarcated as external scope. | **RESOLVED (Scope Bounded)** |
| **C6 — Review Provenance (E-19)** | Claims of "external reviews from Claude and Gemini". | Internal LLM subagent chats mislabeled as external peer reviews. | - Formally documented in `BASELINE_VERIFICATION.md` (Claim E-19) as absent/unverified.<br>- All references to external peer reviews eliminated from drafts. | **RESOLVED (Accurately Labeled)** |

---

## 3. Empirical Tracing Findings (Real Measurements)

From `sentinel_stage_trace.json` (executed via Chromium CDP and Playwright):

| Sentinel Marker Channel | Stage 1: Source HTML | Stage 2: Live DOM | Stage 3: Chromium AXTree | Stage 4a: Default Serializer | Stage 4b: Extended Whitelist | Stage 5: Observation Buffer | Stage 6: Client Payload | Pipeline Outcome |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Visible Typography** (`SENTINEL_TEXT_ALPHA_991`) | **TRUE** | **TRUE** | **TRUE** | **TRUE** | **TRUE** | **TRUE** | **TRUE** | **100% Concordant Survival** |
| **WAI-ARIA on Interactive Button** (`SENTINEL_ARIA_BETA_992`) | **TRUE** | **TRUE** | **TRUE** | **TRUE** | **TRUE** | **TRUE** | **TRUE** | **100% Survival to Model** |
| **WAI-ARIA on Non-Interactive Span** (`SENTINEL_SPAN_ARIA_993`) | **TRUE** | **TRUE** | **TRUE** | **FALSE** | **FALSE** | **FALSE** | **FALSE** | **Critical Divergence** (AXTree preserves, serializer strips) |
| **Custom `data-*` on Interactive Button** (`SENTINEL_DATA_GAMMA_994`) | **TRUE** | **TRUE** | **FALSE** | **FALSE** | **TRUE** | **FALSE\*** | **FALSE\*** | **Reversed Divergence** (Needs runner whitelist injection) |
| **Custom `data-*` on Container** (`SENTINEL_DATA_DELTA_995`) | **TRUE** | **TRUE** | **FALSE** | **FALSE** | **FALSE** | **FALSE** | **FALSE** | **Total Pruning** (Non-interactive tags stripped) |
| **Schema.org JSON-LD in `<script>`** (`SENTINEL_JSONLD_EPSILON_996`) | **TRUE** | **TRUE** | **FALSE** | **FALSE** | **FALSE** | **FALSE** | **FALSE** | **Hardcoded Pruning** (`DISABLED_ELEMENTS`) |
| **HTML `<meta>` Tag** (`SENTINEL_META_ETA_998`) | **TRUE** | **TRUE** | **FALSE** | **FALSE** | **FALSE** | **FALSE** | **FALSE** | **Hardcoded Pruning** (`DISABLED_ELEMENTS`) |

*\*Note: In `browser-use 0.13.10`, `Agent` initializes its own internal `DEFAULT_INCLUDE_ATTRIBUTES` unless patched in the runner context (`protocol_v3_runner.EXTENDED_ATTRIBUTES`).*

---

## 4. Verification and Test Suite Ledger

All offline test suites pass with Exit Code 0:

| Test Script | Scope & Assertions | Exit Code | Verified Outcome |
|---|---|:---:|---|
| `offline_test_suite.py` | 13 comprehensive pipeline, verifier, and schedule tests | **0** | **13/13 PASSED** |
| `test_sentinel_pipeline.py` | 5 unit tests verifying empirical sentinel survival across Stages 1–6 | **0** | **5/5 PASSED** |
| `test_verifier_ground_truth_battery.py` | 12 known-pass and known-fail assertions across tasks T1–T6 | **0** | **12/12 PASSED** |
| `test_treatment_leakage_and_integrity.py` | 6 tests for button label de-confounding, cleanliness, and vision enforcement | **0** | **6/6 PASSED** |
| `test_schedule_validity.py` | 6 tests for Option A (72 runs), Option B (96 runs), and smoke schedules | **0** | **6/6 PASSED** |
| `test_budget_controls.py` | 7 tests for fail-closed budget guard and model pricing bounds | **0** | **7/7 PASSED** |
| `test_mutation_audit.py` | 7 mutation tests verifying test assertions detect verifier breakages | **0** | **7/7 PASSED** |
| `test_power_audit.py` | 7 tests verifying RCBD stratified CMH power and sample size benchmarks | **0** | **7/7 PASSED** |
| `test_observation_pipeline_stages.py` | 5 tests for multi-stage accessibility tree concordance/divergence | **0** | **5/5 PASSED** |
| `test_live_instrumentation_offline.py` | 3 offline integration tests with `FakeListChatModel` & CDP session | **0** | **3/3 PASSED** |
| `audit_claims_and_evidence.py` | Automated claim-evidence guard verifying 0 unearned claims in manuscripts | **0** | **PASSED (0 Violations)** |

**Total passing test cases:** **77 tests across 11 test suites.**

---

## 5. Remaining Scientific Limitations

1. **Lack of Behavioral Model Evidence:** Zero live trials have been executed. The behavioral utility of delivered markup remains an unobserved hypothesis.
2. **Framework Monoculture:** All measurements represent `browser-use 0.13.10`. Behavior in Playwright native AXTree, Puppeteer, Selenium, or BrowserGym requires separate cross-framework evaluation.
3. **Synthetic Toy Fixture:** A 10-product static e-commerce catalog cannot capture dynamic single-page application complexities (shadow DOM, iframes, dynamic hydration).
4. **Statistical Power Ceiling:** A 72-run pilot ($n=20$/arm on primary tasks) has only ~10.8% power to detect $\Delta = 0.20$. It cannot claim channel equivalence if results are non-significant.
5. **Multimodal Disconnect:** Disabling vision (`use_vision=False`) isolates text mechanics, but limits applicability to frontier screenshot-grounded agents (OpenAI Operator, Anthropic Computer Use).
