# Revised Experiment Protocol Proposal (Phase 2 Confirmatory Benchmark)

**Project:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents  
**Timestamp:** 2026-10-24T23:27:00  
**Workspace:** `C:\testing\research_execution_20261018\`  

---

## 1. Protocol Architecture & Treatment Arm Definitions

The proposed Phase 2 Confirmatory Benchmark preserves the rigorous three-arm Randomized Complete Block Design (RCBD) while eliminating the information redundancy confound identified in the Phase 1 pilot.

### Treatment Arms ($K=3$)
1. **Arm 1: `ABS` (Pruned Baseline DOM)**
   - *DOM Representation:* Baseline HTML (`v0-baseline`), stripped of custom `data-*` attributes and non-standard ARIA annotations.
   - *Serialization:* Uses default `browser-use` DOM extraction (`DEFAULT_INCLUDE_ATTRIBUTES`).
   - *Vision Control:* `use_vision=False` (Strict). Eliminates visual multimodal confounds.
2. **Arm 2: `ARIA` (Standard Accessible Name & Role Markup)**
   - *DOM Representation:* Accessible HTML (`v2-aria`), implementing W3C WAI-ARIA 1.2 patterns (`aria-label`, `role`, `aria-checked`, `aria-expanded`).
   - *Serialization:* Evaluates the standard accessibility tree representation used by screen readers and accessibility-first agents.
   - *Vision Control:* `use_vision=False` (Strict).
3. **Arm 3: `DATA-CFG` (Configured Additive Semantic Markup)**
   - *DOM Representation:* Enriched HTML (`v3-data-attrs`), embedding machine-readable microdata attributes (`data-action`, `data-stock-status`, `data-rating`, `data-product-id`).
   - *Serialization:* Preserves extended attribute whitelist (`EXTENDED_ATTRIBUTES`).
   - *Vision Control:* `use_vision=False` (Strict).

---

## 2. Experimental Design: 72-Run Balanced RCBD

- **Block Structure:** 4 sequential blocks of 18 trials each ($4 \times 18 = 72$ total runs).
- **Within-Block Allocation:** Each block contains exactly one replicate of each of the 6 tasks across all 3 arms ($3 \times 6 = 18$ runs per block).
- **Sample Size Allocation:**
  - `ABS`: $N=24$ runs ($4 \text{ blocks} \times 6 \text{ tasks}$).
  - `ARIA`: $N=24$ runs ($4 \text{ blocks} \times 6 \text{ tasks}$).
  - `DATA-CFG`: $N=24$ runs ($4 \text{ blocks} \times 6 \text{ tasks}$).
  - Total: $N=72$ runs.
- **Randomization:** Trial execution order within each block is generated via cryptographically secure pseudo-random permutations to mitigate temporal confounding and provider latency drift.

---

## 3. Statistical Analysis Plan (SAP)

### Primary Outcome
- **Binary Task Success ($Y \in \{0, 1\}$):** Deterministically assessed by independent ground-truth state verifiers (cart contents, order confirmation ID, or grounded refusal classification).

### Primary Inferential Hypothesis & Contrasts
We specify three planned orthogonal contrasts:
1. **Contrast 1 (`ARIA vs. BASELINE`):** Tests whether standard accessible names and roles mitigate DOM serialization loss relative to pruned baseline.
2. **Contrast 2 (`DATA-CFG vs. BASELINE`):** Tests whether explicit data-attribute markup mitigates DOM serialization loss relative to pruned baseline.
3. **Contrast 3 (`ARIA vs. DATA-CFG`):** Tests the comparative efficacy of accessibility-tree representations versus raw data-attribute serializations.

### Statistical Test: Task-Stratified Cochran-Mantel-Haenszel (CMH) Test
Because task difficulty constitutes a natural stratification factor, the primary hypothesis test is the task-stratified CMH test:
$$\chi^2_{\text{CMH}} = \frac{\left( \sum_{i=1}^S \left( a_i - \frac{n_{1i} m_{1i}}{T_i} \right) \right)^2}{\sum_{i=1}^S \frac{n_{1i} n_{2i} m_{1i} m_{2i}}{T_i^2 (T_i - 1)}}$$
Where $S=6$ strata (tasks T1–T6), $a_i$ is treatment successes in stratum $i$, and $T_i$ is stratum sample size.

### Multiplicity Control
Familywise error rate is controlled at $\alpha = 0.05$ using Bonferroni adjustment across the 3 planned contrasts:
$$\alpha_{\text{adj}} = \frac{0.05}{3} \approx 0.0167$$

### Effect Size Estimation
For each pairwise contrast, the Risk Difference ($\text{RD} = p_1 - p_2$) is reported with **95% Newcombe Hybrid Score Confidence Intervals** (Newcombe 1998, Method 10) and **Agresti-Caffo Adjusted Wald Intervals**.

---

## 4. Strict Methodological Rule: Separation of Pilot vs. Confirmatory Data

> [!IMPORTANT]
> The 41 completed runs from the Phase 1 benchmark MUST NOT be pooled with the Phase 2 confirmatory study.

### Why Pooling Is Methodologically and Statistically Prohibited:

1. **Distributional Incommensurability (Data Generation Shift):**
   - In Phase 1, the DOM mockups contained visible text redundancy, creating a 100% ceiling effect.
   - In Phase 2, the DOM mockups will test icon-only buttons and visual glyphs where baseline text is absent.
   - Pooling observations generated under different causal data-generating mechanisms creates an uninterpretable mixture distribution that violates the Gauss-Markov theorem and exchangeability assumptions.

2. **Violation of Pre-Registration & Familywise Error Rate ($\alpha$):**
   - Combining pilot data collected under an abandoned protocol with a newly revised confirmatory protocol is a classic form of post-hoc data blending ("p-hacking" or outcome-dependent pooling).
   - In confirmatory clinical and empirical software trials, pilot data can inform sample sizing and power calculations, but cannot be counted toward primary confirmatory significance testing.

3. **Ceiling Compression Bias:**
   - Injecting 41 trials with a 100% success rate into the new benchmark would artificially compress treatment effect sizes ($\text{RD}$) toward zero and inflate false-negative rates (Type II error).

### Scientific Treatment of Phase 1 Data:
The 41 completed trials in `results/v3_3arm_summary.csv` are formally designated and reported as:
**"Phase 1 Pilot Study: Feasibility, Reliability, and Demonstration of the Baseline Text-Redundancy Confound."**
Phase 2 will be initialized with a clean, dedicated output directory (`results/confirmatory_v4/`) and its own frozen schedule.
