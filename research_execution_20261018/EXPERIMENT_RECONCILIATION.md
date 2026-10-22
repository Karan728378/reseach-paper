# EXPERIMENTAL PROTOCOL RECONCILIATION

**Project:** Autonomous Browser Agent Additive Semantic Markup Study  
**Workspace:** [`C:/testing/research_execution_20261018/`](file:///C:/testing/research_execution_20261018/)  
**Audit Date:** October 21, 2026  

---

## 1. Executive Summary

This document formally reconciles the three distinct experimental protocols discovered in the workspace. They represent successive stages of research maturity and must **never be pooled, combined, or compared as if they belonged to the same study**:

```
                       EVOLUTION OF EXPERIMENTAL PROTOCOLS
┌─────────────────────────┐     ┌─────────────────────────┐     ┌─────────────────────────┐
│  Experiment 1 (Pilot)   │     │ Experiment 1b (Aborted) │     │   Protocol v3 (Current) │
│  - 250 Planned Trials   │ ──> │  - 147 Attempted Trials │ ──> │  - 96 Planned Trials    │
│  - Multimodal Vision    │     │  - Quota Crash (Run 105)│     │  - Strictly Text-Only   │
│  - Fatal Feature Pruning│     │  - Discontinued         │     │  - Hardened Verifiers   │
│  (Invalidated)          │     │  (Truncated)            │     │  (Verified / Pending)   │
└─────────────────────────┘     └─────────────────────────┘     └─────────────────────────┘
```

---

## 2. Comparative Matrix Across All Three Protocols

| Protocol Dimension | Historical Pilot (Exp 1) | Aborted Main Run (Exp 1b) | Current Protocol v3 (Option A) |
| :--- | :--- | :--- | :--- |
| **Execution Period** | October 6–7, 2026 | October 11, 2026 | Frozen October 18, 2026 (Live Pending) |
| **Primary Data Record** | [`results/pilot-summary-clean.csv`](file:///C:/testing/results/pilot-summary-clean.csv) | [`results/main_experiment/full-summary.csv`](file:///C:/testing/results/main_experiment/full-summary.csv) | [`proposed_randomized_schedule.csv`](file:///C:/testing/research_execution_20261018/proposed_randomized_schedule.csv) |
| **Planned Sample Size** | $N = 250$ (5 arms $\times$ 5 tasks $\times$ 10 reps) | $N = 250$ (5 arms $\times$ 5 tasks $\times$ 10 reps) | $N = 96$ (4 arms $\times$ 6 tasks $\times$ 4 reps) |
| **Executed Trials** | 261 raw runs (250 cleaned) | 147 runs (42 quota aborts) | **0 live runs** (Harness validated offline) |
| **Experimental Arms** | `v0-baseline`, `v1-jsonld`, `v2-aria`, `v3-data-attrs`, `v4-evidence-meta` | `v0-baseline`, `v1-jsonld`, `v2-aria`, `v3-data-attrs` | `BASELINE` (ABS), `BASELINE_REP` (VIS), `ARIA`, `DATA-CFG` |
| **Baseline Architecture**| Single baseline (`v0-baseline`) | Single baseline (`v0-baseline`) | Dual baseline arms mapped to `v0-baseline` to test stability |
| **Task Design** | T1–T5 (All positive tasks) | T1–T5 (All positive tasks) | T1–T5 Primary Grounded ($N=80$) + T6 Negative Probe ($N=16$) |
| **Model Modality** | `use_vision=True` (Multimodal pixel input) | `use_vision=True` (Multimodal pixel input) | `use_vision=False` (Strict text-only DOM) |
| **Attribute Handling** | Default library whitelist (Custom `data-*` stripped) | In-memory `inspect.getsource` DOM patch | Enforced runner whitelist (`EXTENDED_ATTRIBUTES`) |
| **JSON-LD Reach** | Stripped by `DISABLED_ELEMENTS` (0% reach) | In-memory DOM hook attempt | Acknowledged unobservable; excluded from primary comparisons |
| **T3 Verifier** | Accepted any audio product (6 SKUs) | Accepted any audio product (6 SKUs) | Strictly requires `wh-002` only (BudPro Wireless X, rating 4.5) |
| **T4 Verifier** | Awarded 0.25 unconditional partial credit | Awarded 0.25 unconditional partial credit | Strictly requires `order_confirmed == True` (0.0 on incomplete) |
| **T5 Verifier** | Checked empty cart without pre-seeding | Checked empty cart without pre-seeding | Asserts `pre_cart_count == 1` before checking empty |
| **T6 Verifier** | Not implemented (Task T6 did not exist) | Not implemented (Task T6 did not exist) | Rewards grounded refusal; scores hallucination as 0.0 |
| **Statistical Model** | Unstratified Friedman test / ANOVA | None (Run aborted) | Task-Stratified Cochran–Mantel–Haenszel & Newcombe CIs |
| **Multiple Testing** | No multiplicity adjustment | None (Run aborted) | Bonferroni-corrected threshold ($\alpha = 0.0167$) |

---

## 3. Why Historical Data Cannot Be Pooled with Protocol v3

Attempting to combine or pool data from Experiment 1 or 1b into Protocol v3 would violate fundamental principles of scientific experimental design:

1. **Modality Incompatibility (`use_vision=True` vs `use_vision=False`):**  
   In Experiments 1 and 1b, the model received full rendered screenshots of the webpage. The agent was able to navigate using visual layout, button colors, and rendered typography, rendering DOM text markup differences largely irrelevant. Protocol v3 tests pure text-based DOM reasoning where the model sees ONLY the text DOM tree.
2. **Treatment Delivery Divergence:**  
   In Experiment 1, custom `data-*` attributes and JSON-LD never entered the LLM prompt. In Protocol v3, `data-*` attributes are verified to reach the prompt via the extended whitelist patch. Pooling them would combine "untreated" trials with "treated" trials under the same label.
3. **Verifier Construct Shift:**  
   In Experiment 1, a run on T3 was scored as a success if the agent added *any* headphone or earbud to the cart (100% artificial ceiling). In Protocol v3, T3 strictly evaluates whether the agent identified the second-highest rated item (`wh-002`). Combining these would contaminate the outcome variable $Y_{ijk}$.
4. **Survivorship Bias Contamination:**  
   Experiment 1's cleaned summary excluded domain failures and retried until success. Protocol v3 logs failures permanently, guaranteeing unbiased effect estimation.

---

## 4. Current Status of Protocol v3

- **Confirmatory Trials:** 0 of 96 scheduled trials executed.
- **Safety Gate:** Line 258 of [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py) remains active (`SAFETY_GATE_LOCKED = True`).
- **Pipeline Demonstration:** Validated using the complete synthetic benchmark (`dataset_1_valid_complete.csv`), 6 local browser mechanics checks, and 4 mock prompt extraction traces.
