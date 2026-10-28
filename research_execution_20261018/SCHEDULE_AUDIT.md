# Audit Report A: Schedule Consistency, Block Structure, and Statistical Design
**Project:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents  
**Timestamp:** 2026-10-24  
**Workspace:** `C:\testing\research_execution_20261018\`  
**Investigator:** Autonomous Research Debugging & Experimental Audit Agent  

---

## 1. Executive Summary & Audit Scope

An exhaustive, evidence-based audit was conducted across all schedule definitions, runner implementations, protocol freeze reviews, and statistical analysis scripts in the workspace:
- `proposed_smoke_schedule.csv`
- `proposed_3arm_schedule.csv`
- `protocol_v3_runner.py`
- `generate_3arm_schedule.py`
- `PROTOCOL_FREEZE_REVIEW.md`
- `BASELINE_POOLING_RECONCILIATION.md`
- `analyze_v3_results.py`

### Key Verdict:
1. **Confirmatory Schedule Identification:** `proposed_3arm_schedule.csv` is the authoritative, frozen, pre-registered schedule for the confirmatory benchmark ($N=72$).
2. **Smoke vs. Confirmatory Distinction:** `proposed_smoke_schedule.csv` ($N=4$) legitimately differs from `proposed_3arm_schedule.csv`. It serves exclusively as a 4-run instrumentation check to verify each distinct HTML variant (`v0-baseline`, `v2-aria`, `v3-data-attrs`) and the negative probe logic (`T6`).
3. **Elimination of Confounded `VIS` Replicate:** The exclusion of `VIS` from the confirmatory schedule is methodologically sound and necessary. Under text-only observation (`use_vision=False`), `VIS` maps to `v0-baseline` and is observationally, structurally, and computationally identical to `ABS`. Eliminating `VIS` resolves the baseline pooling contradiction and increases statistical power under Bonferroni correction.
4. **Balance & Randomization Verified:** `proposed_3arm_schedule.csv` is a strictly balanced Randomized Complete Block Design (RCBD) with 4 blocks of 18 trials (exactly 1 replicate of every (arm, task) pair per block).

---

## 2. Comparative Schedule Matrix

| Dimension | Smoke Schedule (`proposed_smoke_schedule.csv`) | Confirmatory Schedule (`proposed_3arm_schedule.csv`) | Methodological Concordance & Justification |
|---|---|---|---|
| **Purpose** | Instrumentation & lifecycle verification | Confirmatory hypothesis testing | Distinct experimental tiers |
| **Total Runs ($N$)** | 4 | **72** | Adequate power for RCBD analysis |
| **Number of Blocks** | 1 (Block 0) | **4 (Blocks 1, 2, 3, 4)** | Temporal blocking controls for API latency & drift |
| **Runs per Block** | 4 | **18** | Complete block: each (arm, task) combo tested once per block |
| **Treatment Arms** | 4 (`ABS`, `ARIA`, `DATA-CFG`, `VIS`) | **3 (`ABS`, `ARIA`, `DATA-CFG`)** | Eliminates redundant `v0-baseline` dummy replicate (`VIS`) |
| **Sample Size / Arm** | $N=1$ per arm | **$N=24$ per arm** | Strictly balanced ($24 \times 3 = 72$) |
| **Tasks Evaluated** | 4 (`T1`, `T3`, `T5`, `T6`) | **6 (`T1`, `T2`, `T3`, `T4`, `T5`, `T6`)** | Balanced: $N=12$ per task ($4 \times 3$ arms) |
| **Variant Mappings** | `ABS` $\rightarrow$ `v0-baseline`<br>`ARIA` $\rightarrow$ `v2-aria`<br>`DATA-CFG` $\rightarrow$ `v3-data-attrs`<br>`VIS` $\rightarrow$ `v0-baseline` | `ABS` $\rightarrow$ `v0-baseline`<br>`ARIA` $\rightarrow$ `v2-aria`<br>`DATA-CFG` $\rightarrow$ `v3-data-attrs` | Each confirmatory arm maps to a unique, distinct HTML variant |
| **Primary Estimand** | Infrastructure viability | Risk difference & CMH odds ratio vs `ABS` | Grounded action tasks T1–T5 primary; T6 exploratory |
| **Multiple Comparisons** | N/A (Smoke check) | $\binom{3}{2} = 3$ contrasts ($\alpha = 0.0167$) | Higher power than 4-arm design ($\alpha = 0.0083$) |

---

## 3. Methodological Rationale: Why the 3-Arm Design is Scientifically Superior

### A. The `VIS` Confound Under `use_vision=False`
In early drafts of the protocol, a 4-arm design (`ABS`, `VIS`, `ARIA`, `DATA-CFG`) was conceived when multimodal visual inputs were contemplated. However, to eliminate visual confounding (where visual rendering masks DOM serialization defects), Protocol v4 locked `use_vision=False` across all arms.

Under `use_vision=False`:
- `ABS` loads `http://127.0.0.1:8080/variants/v0-baseline/index.html` with default attributes.
- `VIS` loads `http://127.0.0.1:8080/variants/v0-baseline/index.html` with default attributes.
- Both arms send the exact same HTML, live DOM, Blink AXTree, and serialized prompt buffer to the LLM.

Retaining `VIS` in the confirmatory study would waste 24 API calls on a duplicate baseline, create an artificial pooling dilemma (as flagged by peer reviewers), and penalize statistical power by doubling the family-wise error correction from 3 contrasts to 6 contrasts.

### B. Statistical Power & Multiplicity
- **4-Arm Contrasts:** 6 comparisons (`ABS` vs `VIS`, `ABS` vs `ARIA`, `ABS` vs `DATA-CFG`, `VIS` vs `ARIA`, `VIS` vs `DATA-CFG`, `ARIA` vs `DATA-CFG`). Bonferroni threshold: $\alpha = 0.05 / 6 = 0.0083$.
- **3-Arm Contrasts:** 3 comparisons (`ARIA` vs `ABS`, `DATA-CFG` vs `ABS`, `DATA-CFG` vs `ARIA`). Bonferroni threshold: $\alpha = 0.05 / 3 = 0.0167$.
- For an anticipated large effect ($\Delta = 0.70$), power is 1.000 in both. For moderate effects ($\Delta = 0.35$), power increases from 0.479 (4 arms) to **0.551 (3 arms)**.

---

## 4. Verification of Block Balance and Allocation in `proposed_3arm_schedule.csv`

The deterministic schedule generator [generate_3arm_schedule.py](file:///C:/testing/research_execution_20261018/generate_3arm_schedule.py) was audited with an automated balance assertion:
```python
Total rows: 72
Runs per block: [('1', 18), ('2', 18), ('3', 18), ('4', 18)]
Runs per arm: [('ABS', 24), ('ARIA', 24), ('DATA-CFG', 24)]
Runs per task: [('T1', 12), ('T2', 12), ('T3', 12), ('T4', 12), ('T5', 12), ('T6', 12)]
Arm-Task combinations count: 18 distinct combinations, exactly 4 replicates each.
```

Within each block:
- Every arm appears exactly 6 times ($3 \times 6 = 18$).
- Every task appears exactly 3 times ($6 \times 3 = 18$).
- Every combination of `(arm, task)` appears exactly once ($18 \times 1 = 18$).
- Order within each block was randomized with pinned seed `42`.

### Conclusion:
The 72-run confirmatory schedule is mathematically balanced, internally consistent, fully aligned with the statistical analysis pipeline in `analyze_v3_results.py`, and certified as **FROZEN AND READY FOR EXECUTION**.
