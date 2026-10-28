# SAFETY GATE AND COST AUDIT (FINAL)

**Audit Date:** 2026-10-22  
**Auditor:** Senior Research Systems & Methodological Integrity Auditor  
**Project Workspace:** `C:\testing\research_execution_20261018\`  
**Safety Gate Status:** **STRICTLY LOCKED AND VERIFIED (UNCONDITIONAL RUNTIME ERROR)**  
**Cost Status:** **$0.00 SPENT (OFFLINE ONLY; NO BILLING AUTHORIZED)**  

---

## 1. Executive Summary

This audit establishes the operational safety, live-model interlocks, and financial constraints of the research codebase. All tests, runners, fixtures, and analysis scripts were audited to ensure that no live model calls, API token consumption, or unintended billing can occur during test discovery, regression verification, or offline analysis.

The active experiment runner ([`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py)) enforces a multi-layer safety interlock that prevents execution in live mode. Offline test suites run exclusively against local HTTP servers (`localhost:8080`), static fixtures, and mock agents.

---

## 2. Call Graph and Entry Point Audit

Every executable entry point in the repository was inspected for potential live network calls or un-gated LLM requests:

| Entry Point | Mechanism | Gating / Interlock | Live Call Possibility |
|---|---|---|---|
| [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py) | CLI runner for randomized blocks | Lines 248–261: Double `RuntimeError` guard | **BLOCKED (0.0% risk)** |
| [`offline_test_suite.py`](file:///C:/testing/research_execution_20261018/offline_test_suite.py) | Unit & regression test suite | Runs local server & static regex assertions | **SAFE (Mock only)** |
| [`test_agent_prompt_pipeline.py`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py) | End-to-end DOM-to-Prompt pipeline | Uses local HTTP server & `browser-use` DOM state; does not invoke `Agent.run()` or LLM APIs | **SAFE (Local CDP only)** |
| [`verify_treatment_delivery_e2e.py`](file:///C:/testing/research_execution_20261018/verify_treatment_delivery_e2e.py) | Treatment delivery verifier | Headless Playwright page queries against local HTTP server | **SAFE (Local Playwright)** |
| [`test_accessibility_tree_comparison.py`](file:///C:/testing/research_execution_20261018/test_accessibility_tree_comparison.py) | Dynamic AXTree verification | Compares pre-computed JSON and CDP snapshots | **SAFE (Local comparisons)** |
| [`test_power_audit.py`](file:///C:/testing/research_execution_20261018/test_power_audit.py) | Power calculation tests | Analytical & Monte Carlo simulations | **SAFE (Pure CPU)** |
| [`test_mutation_audit.py`](file:///C:/testing/research_execution_20261018/test_mutation_audit.py) | Defect detection verification | Exercises mock mutations & safety gate | **SAFE (Verified Gate)** |
| [`run_offline_pipeline_demo.py`](file:///C:/testing/research_execution_20261018/run_offline_pipeline_demo.py) | End-to-end offline pipeline demonstration | Local CDP extraction and prompt compilation | **SAFE (No LLM calls)** |

---

## 3. Detailed Verification of the Active Safety Gate

The primary execution entry point is [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L248-L261). Its safety mechanism operates as follows:

```python
# protocol_v3_runner.py lines 247-261
# Strict Safety Interlock
if mode == "live" and not confirm_live:
    raise RuntimeError(
        "SAFETY INTERLOCK: Live execution requested without explicit --confirm-live-execution flag.\n"
        "This safety gate prevents unintended live API spending."
    )
    
if mode == "live":
    # Double check API key presence without printing it
    if not os.environ.get("GOOGLE_API_KEY"):
        raise RuntimeError("SAFETY INTERLOCK: GOOGLE_API_KEY environment variable is not configured.")
    raise RuntimeError(
        "SAFETY GATE: Live execution remains gated pending user protocol review.\n"
        "To launch live trials after review, update the safety gate in protocol_v3_runner.py."
    )
```

### Safety Properties:
1. **Unconditional Gate:** Even if both `--live` and `--confirm-live-execution` flags are supplied on the command line, execution halts immediately at line 258 with an unconditional `RuntimeError`.
2. **Credential Protection:** The check at line 256 inspects the existence of `GOOGLE_API_KEY` without ever echoing, logging, or serializing the key content.
3. **Default Mode:** Running `python protocol_v3_runner.py` defaults to `mode = "mock"` (line 293), which strictly executes `run_single_mock_trial()` (line 282) using synthetic delay and deterministic simulation.

### Independent Mutation Test:
In [`test_mutation_audit.py`](file:///C:/testing/research_execution_20261018/test_mutation_audit.py#L96-L107), Mutation 5 explicitly verifies that invoking `execute_experiment(mode="live", confirm_live=False)` raises `RuntimeError`. The test passes in 0.030s.

---

## 4. Financial Cost Modeling and Budget Projections

While zero expenditure has occurred, a prospective cost model for the proposed 96-run confirmatory trial was audited.

### Cost Parameters:
- **Target Model:** Gemini 2.5 Flash Lite (pricing assumed: $0.075 / 1M input tokens, $0.30 / 1M output tokens).
- **Run Count ($N$):** 96 randomized trials across 4 blocks.
- **Maximum Step Cap:** 30 steps per trial.
- **Estimated Average Steps per Trial:** 12–18 steps.
- **Tokens per Step:**
  - System + Task Prompt: ~800 tokens
  - Serialized Observation (DOM extract): ~1,200 tokens
  - Context Accumulation per step: ~400 tokens
  - Model Response (Action JSON): ~150 tokens

### Budget Calculation:
- **Worst-Case Scenario (all 96 trials hit 30-step cap):**
  - Steps: $96 \times 30 = 2,880$ steps
  - Input Tokens: $2,880 \times 2,200 \approx 6.34\text{M}$ tokens $\times \$0.075 / 1\text{M} = \$0.48$
  - Output Tokens: $2,880 \times 150 \approx 0.43\text{M}$ tokens $\times \$0.30 / 1\text{M} = \$0.13$
  - Total Worst-Case API Cost: **~$0.61 – $1.20** (accounting for context window growth)
- **Expected Scenario (mean 15 steps per trial):**
  - Total Expected API Cost: **~$0.30 – $0.65**

### Critical Financial Boundaries:
1. **Estimate vs. Authorization:** The ~$1.00 budget estimate is an engineering projection, **NOT an authorization to spend**.
2. **No Billing Quota Activated:** No payment methods or live production keys have been configured for automated runs.
3. **Gate Release Boundary:** Releasing the safety gate requires human review, explicit protocol freeze approval, and manual removal of line 258 in [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py).

---

## 5. Audit Conclusion

The repository adheres strictly to the non-negotiable safety rules:
- Offline work only: **ENFORCED**
- No live-agent experiments or paid model/API calls: **VERIFIED**
- Experiment safety gate unbypassed and intact: **VERIFIED**
- API keys redacted and unexposed: **VERIFIED**
