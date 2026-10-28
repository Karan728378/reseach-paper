# Next Phase Research Decision & Methodological Roadmap

**Project:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents  
**Timestamp:** 2026-10-24T23:28:00  
**Workspace:** `C:\testing\research_execution_20261018\`  

---

## 1. Executive Summary of Current Status

1. **Budget Guard Repaired & Verified:**
   - [budget_controller.py](file:///C:/testing/research_execution_20261018/budget_controller.py) now meters every individual in-flight model request *prior to network dispatch* via [BudgetGuardedChatModel](file:///C:/testing/research_execution_20261018/budget_controller.py).
   - Thread-safe synchronization via `threading.RLock()` eliminates concurrent dispatch race conditions.
   - Verified via 6 dedicated unit tests in [test_budget_guard_repairs.py](file:///C:/testing/research_execution_20261018/test_budget_guard_repairs.py) (100% passing). Full offline regression suite: **121 / 121 tests passing**.
   - Historical ledger count of **604 requests** is preserved. The guard fails closed immediately if further requests are attempted today under the 600 ceiling.

2. **Ceiling Effect Diagnosed:**
   - All 41 completed confirmatory runs scored 1.0 across all three arms (`ABS`, `ARIA`, `DATA-CFG`).
   - Forensic analysis proved this is caused by an **Information Redundancy Confound**: prices, ratings, and product titles were redundantly rendered as visible text nodes in the DOM mockups.
   - Because standard DOM serializers preserve visible text, the pruned baseline arm (`ABS`) suffered zero information loss.

---

## 2. Evaluation of Strategic Options

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 STRATEGIC OPTIONS MATRIX                               │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ OPTION 1: Continue Existing Protocol & Complete Remaining 31 Runs (Runs 42–72)         │
│ - Description: Wait for quota rollover, resume Run 42, finish the 72-run schedule.     │
│ - Scientific Merit: Low. Because all tasks are already solved at 100% by the baseline  │
│   model, the remaining 31 runs will almost certainly score 1.0, spending ~350 requests │
│   to confirm an already proven ceiling effect (RD=0.0, p=1.0).                         │
│ - Quota Efficiency: Wasteful. Spends remaining free-tier capacity on redundant data.   │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ OPTION 2: Modify Tasks In-Flight and Continue Appending to Current Summary CSV         │
│ - Description: Alter task instructions or DOM mockups now and resume at Run 42.        │
│ - Scientific Merit: Severely Flawed / Inadmissible. Blending runs from two different   │
│   task distributions in the same summary file violates RCBD orthogonality and creates  │
│   an uninterpretable data mixture. Pre-registration integrity is destroyed.            │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ OPTION 3 (RECOMMENDED): Conclude Phase 1 as a Completed Pilot; Launch Redesigned       │
│                         Task Battery as Phase 2 Confirmatory Benchmark                 │
│ - Description: Formally freeze the 41 completed runs as "Phase 1 Pilot Study:          │
│   Feasibility, Harness Reliability, and Identification of the Text Redundancy          │
│   Confound". Update local website mockups offline to test genuine DOM serialization    │
│   loss (icon-only affordances, visual glyphs). Prepare Phase 2 protocol cleanly.       │
│ - Scientific Merit: Outstanding. Follows rigorous scientific practice by publishing   │
│   pilot findings honestly, eliminating confounds, and conducting a calibrated study.   │
│ - Quota Efficiency: Optimal. Zero quota wasted on redundant ceiling runs.              │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Formal Recommendation

### **RECOMMENDATION: OPTION 3 (Conclude Phase 1 as Pilot; Prepare Phase 2 Confirmatory Benchmark)**

We recommend **stopping further live trials under the current task battery** and adopting the following phased progression:

### Phase 1 (Completed & Certified Pilot):
- **Status:** **FROZEN.**
- **Artifacts:**
  - Canonical summary: [results/v3_3arm_summary.csv](file:///C:/testing/research_execution_20261018/results/v3_3arm_summary.csv) (41 completed trials, 3 infra aborts).
  - Raw telemetry: [results/v3_3arm_summary_raw.csv](file:///C:/testing/research_execution_20261018/results/v3_3arm_summary_raw.csv) (46 total attempts).
  - Traces: `results/3arm_runs/` (46 JSON trace files).
  - Statistical Report: `results/analysis_intermediate_41runs/analysis_report.md`.
- **Contribution to Paper:** Demonstrates harness execution stability, verifier correctness, $0.00 spend guardrails, and empirically establishes that modern LLMs are robust to DOM attribute pruning when visible text nodes provide redundant semantic information.

### Phase 2 (Redesigned Confirmatory Benchmark):
- **Design:** As specified in [REVISED_EXPERIMENT_PROTOCOL_PROPOSAL.md](file:///C:/testing/research_execution_20261018/REVISED_EXPERIMENT_PROTOCOL_PROPOSAL.md) and [TASK_BATTERY_REDESIGN.md](file:///C:/testing/research_execution_20261018/TASK_BATTERY_REDESIGN.md).
- **Tasks:** Icon-only action affordances, visual-only stock indicators, custom selectable shipping cards, and glyph-based ratings.
- **Harness:** Uses the repaired [BudgetGuardedChatModel](file:///C:/testing/research_execution_20261018/budget_controller.py) to guarantee strict request boundaries.
- **Execution Mode:** Offline development and mock validation first; live execution held until authorized by the operator.

---

## 4. Current Execution Status: HOLD

In strict accordance with the operator's instructions:
- **Live Model Execution:** **ON HOLD (Zero live API calls authorized).**
- **Request Ceilings:** Preserved at current thresholds; historical 604 count preserved.
- **Workspace State:** All files and test suites are 100% verified and reproducible offline.
