# PROTOCOL FREEZE DECISION (FINAL)

**Decision Date:** 2026-10-22  
**Auditor / Review Board:** Antigravity Senior Research Systems & Methodological Integrity Auditor  
**Workspace:** `C:\testing\research_execution_20261018\`  
**Target Protocol:** Protocol v4 (Randomized Complete Block Design, 4 Arms, 6 Tasks, 4 Blocks)  

---

## 1. Multi-Gate Evaluation Framework

In accordance with Section 19 of the Master Execution Specification, the research project is audited across four independent gates. A pass at one gate does not imply a pass at subsequent gates.

```
+-----------------------------------+-----------------------------------+
| GATE                              | DECISION                          |
+-----------------------------------+-----------------------------------+
| Gate A: Offline Engineering       | FULL GO                           |
|         Correctness               | (Full pipeline verified; T6       |
|                                   |  grounded refusal merged & tested)|
+-----------------------------------+-----------------------------------+
| Gate B: Protocol Freeze Readiness | GO (PREFLIGHT READY)              |
|                                   | (Protocol internally consistent;  |
|                                   |  ready pending scope & API key)   |
+-----------------------------------+-----------------------------------+
| Gate C: Empirical Performance     | NO-GO                             |
|         Validity                  | (Zero valid confirmatory trials;  |
|                                   |  historical pilot invalid)        |
+-----------------------------------+-----------------------------------+
| Gate D: Live-Experiment           | NO-GO (STRICTLY LOCKED)           |
|         Authorization             | (Safety gate strictly locked;     |
|                                   |  awaiting explicit human sign-off)|
+-----------------------------------+-----------------------------------+
```

---

## 2. Gate-by-Gate Audit Justification

### Gate A: Offline Engineering Correctness
- **Decision:** **FULL GO**
- **Evidence:**
  - The DOM serialization gap is empirically verified via real Playwright and CDP tree extraction: JSON-LD is 100% pruned, static `aria-label` spans are 100% pruned, interactive ARIA is preserved, and custom `data-*` attributes are conditionally delivered via whitelist.
  - End-to-end prompt extraction (`test_agent_prompt_pipeline.py`) passes 11/11 assertions.
  - Treatment delivery (`verify_treatment_delivery_e2e.py`) passes 8/8 assertions.
  - Tasks T1–T5 verifiers are audited, strict binary scoring is enforced, and non-operational partial credit is removed.
  - Task T6 grounded-refusal verifier is merged into the active runner [`protocol_v3_runner.py:124-190`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L124) and verified via 44-case regression battery in [`offline_test_suite.py`](file:///C:/testing/research_execution_20261018/offline_test_suite.py) (13/13 PASS). Offline test suite passes with 0 failures.

### Gate B: Protocol Freeze Readiness
- **Decision:** **CONDITIONAL GO**
- **Evidence:**
  - Treatment definitions (v0 Baseline, v2 ARIA, v3 DATA-CFG) are isolated without label leakage.
  - Endpoint definitions ($Y \in \{0, 1\}$ evaluated on client state) are locked.
  - Primary inferential model (Task-Stratified Cochran-Mantel-Haenszel test with Bonferroni correction $\alpha = 0.0167$) is codified in `analyze_v3_results.py`.
  - The mandatory non-equivalence rule is codified (non-significant findings cannot be declared equivalence).
  - Randomized schedule with 4 blocks of 24 runs (seed 42) is pre-generated in `proposed_randomized_schedule.csv`.
  - **Condition:** The researcher must select between the exploratory pilot ($N=96$, power $10.85\%$) and the confirmatory trial ($N=480$, power $80.2\%$) to formally freeze the sample size.

### Gate C: Empirical Performance Validity
- **Decision:** **NO-GO**
- **Evidence:**
  - Historical pilot datasets (`pilot-summary-clean.csv`, `full-summary.csv`) are scientifically invalid for claiming semantic markup efficacy:
    1. Treatment variants (v2 ARIA, v3 DATA-CFG) were completely omitted from historical execution (100% of historical runs were executed on v0).
    2. Retry-until-success logic inflated historical success rates to 99.6% through survivorship bias.
    3. Multi-modal vision was enabled (`use_vision=True`), bypassing text-based serialization bottlenecks.
    4. Task T3 accepted 6 SKUs instead of target `wh-002`, and Task T4 awarded unearned partial credit (0.25).
  - No valid confirmatory live-agent runs have yet been executed under Protocol v4.
  - **Action Required:** Historical data must remain strictly descriptive. All performance claims must await post-freeze randomized trials.

### Gate D: Live-Experiment Authorization
- **Decision:** **NO-GO (STRICTLY LOCKED)**
- **Evidence:**
  - The active safety gate at line 258 of [`protocol_v3_runner.py`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L258) throws an unconditional `RuntimeError`.
  - Zero live API calls or paid billing have occurred ($0.00 spent).
  - Multi-agent mutation tests confirm that attempting to execute in live mode triggers the interlock.
  - **Action Required:** A human researcher must review the complete audit findings, approve the T6 verifier patch, confirm the sample size budget, and explicitly remove the code safety gate.

---

## 3. Final Recommendation

The research project represents an outstanding, rigorous offline systems investigation of the DOM serialization bottleneck in autonomous web agents. The systems audit and offline evidence are reproducible and publication-grade as an observation pipeline analysis.

However, **live execution is not authorized**, and **no claims of agent performance differences are defensible today**. Protocol v4 is a verified **Freeze Candidate** ready for human sign-off.
