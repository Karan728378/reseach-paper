# EXPERIMENTAL PROTOCOL SPECIFICATION: DISAMBIGUATION PROBES (PROBE A, PROBE B, AND CONTROL)

**Document Status:** Pre-Registered Protocol Specification & Offline Readiness Audit  
**Project Workspace:** `C:\testing\research_execution_20261018`  
**Target Backend:** Groq API (`openai/gpt-oss-120b`) / Text-Only Browser Automation (`browser-use 0.13.10`)  
**Safety Gate:** `SAFETY_GATE_LOCKED = True` (Zero Live Calls Executed During This Pass)

---

## 1. Experimental Motivation & Research Question

In preliminary exploratory pilot testing (Runs 1–41), the autonomous browser agent achieved a ceiling effect ($100\%$ task completion across ABS, ARIA, and DATA-CFG arms). In that initial task suite, visible typography alone was sufficient to disambiguate target products, rendering additive semantic markup functionally redundant.

To establish whether observation-pipeline pruning bottlenecks induce genuine behavioral divergence when visible typography is insufficient, we specify three controlled disambiguation probes:

1. **Probe A (Custom Attribute Isolation):**
   * *Hypothesis:* When target identity is encoded exclusively in a custom developer attribute (`data-product-id="target-sku-101"`) on interactive buttons with identical visible labels (`"Select Item"`), agents in the default observation pipeline ($\textsc{ABS}$) must guess at random ($50\%$), whereas agents with the extended whitelist ($\textsc{DATA-CFG}$) can observe the attribute and achieve high accuracy ($>90\%$).
2. **Probe B (Container Span ARIA Isolation):**
   * *Hypothesis:* When target identity is encoded in a container `<span>`'s `aria-label`, serializer tag-pruning in `browser-use 0.13.10` (`serializer.py:1046`) purges the non-interactive span and its accessible label from the prompt buffer. Both $\textsc{ABS}$ and $\textsc{DATA-CFG}$ conditions receive identical unaugmented text, proving an observation-pipeline reachability failure rather than an agent behavioral failure.
3. **Positive Control (Rendered Typography):**
   * *Hypothesis:* When target identity is explicitly rendered in the visible text (`SKU: target-sku-101`), agents in all conditions observe the identity and successfully complete the task, confirming basic instruction-following competence.

---

## 2. Experimental Design and Units of Analysis

### 2.1 Independent Experimental Unit
The independent experimental unit is defined as **one freshly spawned browser session executing one discrete trial on a clean browser context with isolated session state**. An execution attempt corresponds to exactly one trial specification.

### 2.2 Treatment Arms and Interventions
* **Arm 1: Negative Baseline ($\textsc{ABS}$):** Default `browser-use 0.13.10` observation pipeline using `DEFAULT_INCLUDE_ATTRIBUTES`. Custom attributes (`data-*`) are stripped.
* **Arm 2: Configured Developer Attributes ($\textsc{DATA-CFG}$):** Runner injects `EXTENDED_ATTRIBUTES` including `data-product-id`, `data-action`, etc. Custom attributes on interactive elements reach the prompt buffer.
* **Arm 3: Positive Control:** Executed across both configurations to establish baseline model reasoning validity.

### 2.3 Position Randomization & Spatial Deconfounding
To prevent models from solving the task via position bias (e.g., always selecting Option 1):
* Every trial specification is assigned a deterministic pseudo-random seed $S_i$.
* If $S_i \pmod 2 = 1$, the positions of the target card and distractor card are swapped via URL query parameter `?swap=true`.
* Target and distractor occupy left/right (or top/bottom) positions with exact $50:50$ probability across blocks.

### 2.4 Randomized Complete Block Design (RCBD)
* Minimum Planning Sample: $N = 40$ trials per probe ($20$ trials in $\textsc{ABS}$, $20$ trials in $\textsc{DATA-CFG}$ across $4$ balanced blocks of $10$ runs).
* Within each block, trials alternate conditions and position seeds deterministically.

---

## 3. Strict Pre-Registered Decision Rules and Multiplicity Correction

### 3.1 Primary Endpoint
* **Primary Outcome ($Y \in \{0, 1\}$):** Verified target selection (`window.SELECTION_SUCCESS == True` evaluated in CDP state).
* **Failure ($Y = 0$):** Selection of distractor SKU, step budget exhaustion, or out-of-domain interaction.

### 3.2 Statistical Comparison and Multiple Testing Correction
* Primary test: Two-tailed Fisher's exact test comparing $\textsc{DATA-CFG}$ vs $\textsc{ABS}$ on Probe A.
* Nominal significance level: $\alpha = 0.05$.
* Bonferroni multiplicity adjustment across probe families: $\alpha_{\text{adj}} = 0.05 / 2 = 0.025$.

### 3.3 Power and Minimum Detectable Effect (MDE)
* With $n = 20$ per arm:
  * If $\textsc{ABS}$ performs at chance ($p_1 = 0.50$), detecting a true $\textsc{DATA-CFG}$ success rate of $p_2 = 0.90$ ($\Delta = 0.40$) achieves $\approx 78\%$ power at $\alpha = 0.025$.
  * However, for moderate effect sizes ($\Delta = 0.20$), power is $<15\%$.
  * *Methodological Constraint:* $N=20$ is a pilot planning minimum. A non-significant result must **never** be interpreted as evidence of equivalence.

---

## 4. Execution Readiness and Operational Safety Gates

### 4.1 Target Model Pinning
* **Provider:** Groq Cloud API
* **Model ID:** `openai/gpt-oss-120b`
* **Temperature:** $0.0$ (deterministic greedy decoding)
* **Max Agent Steps Per Run:** $5$ steps (targeted single-action task)

### 4.2 Budget Guard Ceiling
* **Daily Ledger:** [`results/daily_groq_quota_ledger.json`](file:///C:/testing/research_execution_20261018/results/daily_groq_quota_ledger.json)
* **Spending Cap:** $\$0.00$ USD (fail-closed pre-dispatch enforcement via `LocalBudgetGuard`)
* **Live Execution Authorization Status:** **LOCKED**. Live experiments are NOT executed during this task and require explicit human researcher authorization (`--live --confirm-live-execution`).
