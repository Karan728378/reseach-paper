# AUDIT REPORT: DEFENSIBLE BUDGET CONTROLS AND PREFLIGHT COST ESTIMATION

**Document ID:** `audit_20261022_final/BUDGET_AND_COST_CONTROLS.md`  
**Date:** 2026-10-22  
**Status:** IMPLEMENTED AND INDEPENDENTLY VERIFIED (`test_budget_controls.py` - 7/7 PASS)  
**Protocol:** Protocol v4 (RCBD 4 Arms x 6 Tasks x 4 Blocks)

---

## 1. Executive Summary & Defect Remediation

Prior audits uncovered a significant deficiency in the active runner's financial safety implementation:
1. **Misleading Nomenclature:** The local ceiling of `$10.00` USD was described in logs and reports as a "Hard Cost Ceiling", implying an inviolable financial limit.
2. **Post-Hoc Accumulator:** Cost was computed only after a run completed, multiplying `total_steps * 7000` tokens at a hardcoded price.
3. **No Preflight Bound:** No mathematical verification was conducted before launching trial 1 to determine if the scheduled batch could exceed the budget.
4. **Unbounded Unknown Models:** If an unlisted or expensive model was passed, the runner had no pricing lookup and defaulted silently.

To rectify these vulnerabilities, we implemented `budget_controller.py` and integrated it into `protocol_v3_runner.py`, accompanied by a dedicated 7-test regression suite (`test_budget_controls.py`).

---

## 2. Technical Architecture of the Budget Controller

### 2.1 Pricing Table and Fail-Closed Policy
`budget_controller.py` maintains an authoritative pricing registry (`MODEL_PRICING_TABLE`) for Gemini, Anthropic, and OpenAI models.
- **Fail-Closed Enforcement:** If an unknown model is requested (e.g., `get_model_pricing("unsupported-llm")`), the system immediately raises `UnknownModelPricingError`. It strictly refuses to execute without verifiable, bounded financial rates.
- **Rates for Primary Model (`gemini-flash-lite-latest`):**
  - Input tokens: `$0.15` per 1,000,000 tokens.
  - Output tokens: `$0.60` per 1,000,000 tokens.

### 2.2 Preflight Worst-Case and Realistic Bounding
The preflight check now bounds the entire schedule prior to trial 1:
$$\text{Worst-Case Single Trial} = N_{\text{max\_steps}} \times \left(T_{\text{in\_max}} \times P_{\text{in}} + T_{\text{out\_max}} \times P_{\text{out}}\right)$$
Where:
- $N_{\text{max\_steps}} = 30$
- $T_{\text{in\_max}} = 10,000$ tokens/step
- $T_{\text{out\_max}} = 500$ tokens/step
- For `gemini-flash-lite-latest`:
  - Worst-case single trial: $30 \times (0.0015 + 0.0003) = \$0.0450$ USD.
  - Across $N=96$ runs: $96 \times \$0.0450 = \$4.32$ USD.
  - Realistic expected cost (avg 5.5 steps, ~6,500 in tokens): $96 \times \$0.0055 = \$0.53$ USD.

Because $\$4.32 \le \$10.00$, the preflight check certifies that the 96-run schedule cannot breach the `$10.00` ceiling even under pathological maximum-step conditions.

### 2.3 `LocalBudgetGuard` & Fail-Closed Trial Dispatch
The `LocalBudgetGuard` class manages execution bounds:
- **`check_can_dispatch_trial()`:** Inspects remaining balance before dispatching a trial. If remaining balance $\le 0$, it halts with `[BUDGET ABORT]`.
- **Headroom Mode (`require_worst_case_headroom=True`):** If enabled, verifies that remaining budget $\ge \text{Worst-Case Single Trial}$ before dispatching.
- **Fallback on Missing Metadata:** If a provider fails to return usage metadata, the guard substitutes conservative upper bounds ($10,000$ in / $500$ out) rather than recording zero tokens.

---

## 3. Honest Disclaimer on Local Software Guardrails

> [!WARNING]
> **Client-Side Guard Limitation:**
> The local cost ceiling in `protocol_v3_runner.py` is a **client-side software guardrail**, NOT a provider-side financial quota.
>
> If a cloud provider experiences billing latency, if a network timeout disconnects the client while a streaming generation is billed upstream, or if an invalid API key configuration triggers unauthorized billing loops, a local process cannot prevent provider-side charges.
>
> **Mandatory Live Prerequisites:**
> Before any live trial is authorized:
> 1. A hard spending budget must be configured in the Google Cloud Billing Console (e.g. Budget Alert with automated Pub/Sub project disablement at $\le \$15.00$).
> 2. API keys must have IP and API restrictions enabled.
> 3. Initial verification runs must use the 4-run smoke schedule (`proposed_smoke_schedule.csv`, budget $\le \$0.20$) before the full pilot.

---

## 4. Test Verification Evidence

The budget control suite was executed using:
`python -m unittest research_execution_20261018/test_budget_controls.py`

```text
Ran 7 tests in 0.001s
OK
```

| Test Name | Verifies | Result |
| :--- | :--- | :--- |
| `test_01_unknown_model_fails_closed` | Unknown models raise `UnknownModelPricingError` | PASS |
| `test_02_known_models_return_accurate_pricing` | Gemini/Claude/GPT models have positive rates | PASS |
| `test_03_preflight_budget_calculation` | Bounded worst-case and expected batch costs | PASS |
| `test_04_preflight_fails_when_ceiling_is_too_low` | Flags fail-closed warning when budget < worst-case | PASS |
| `test_05_local_guard_accumulates_and_stops_at_ceiling` | Halts dispatch when ceiling breached | PASS |
| `test_06_guard_fails_closed_on_insufficient_headroom` | Prevents starting run when headroom < 1 trial | PASS |
| `test_07_missing_tokens_fallback_to_conservative_bounds` | Replaces null tokens with conservative bounds | PASS |
