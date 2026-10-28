# REMEDIATION 02: CAUSAL IDENTIFICATION AND EXPERIMENTAL DESIGN
## Project: The DOM Serialization Gap — Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents
**Date:** 2026-10-26  
**Auditor:** Causal Inference and Experimental Methodology Team  

---

## 1. Executive Summary

Autonomous web agent evaluations frequently suffer from observational confounds that undermine causal claims. When assessing whether "semantic markup" enhances LLM agent performance, standard experimental designs inadvertently alter both semantic metadata AND lexical information location.

This audit establishes the formal causal framework, identifies the Action-Label Co-Location Confound, specifies the planned contrasts, and details the four-arm randomized complete block design (RCBD) required for valid causal identification.

---

## 2. Directed Acyclic Graph (DAG) and Observation Pipeline

```
           [Underlying DOM Structure (HTML Source)]
                       |                     \
                       v                      v
             [Accessibility Tree]      [Tag/Attribute Pruner]
                       |                      |
                       v                      v
           [Pruned Serializer Output (Stage 4)]
                       |
                       +-----> [Prompt Assembly (Stage 5)]
                                      |
                                      v
                             [LLM Agent Policy]
                                      |
                                      v
                               [Task Success Y]
```

### Potential Confounders in Naive Evaluations:
1. **Lexical Co-Location ($C_{\text{loc}}$):** Entity name moved onto interactive element vs kept in parent container.
2. **Observation Length ($C_{\text{len}}$):** Adding attributes increases prompt token count, potentially diluting attention.
3. **Task Ceiling Effects ($C_{\text{ceil}}$):** Standard web tasks are solvable from raw visible text alone, reducing treatment variance to zero.

---

## 3. The Action-Label Co-Location Confound

### 3.1 Structural Mechanism
In standard web accessibility implementations, an interactive button associated with an entity is augmented with an `aria-label`:

```html
<!-- Condition 1: BASELINE_ABS (Relational Binding Required) -->
<div class="product-card">
  <h3>SoundFlow Air 3</h3>
  <span class="price">$79.99</span>
  <button>Add to Cart</button>
</div>

<!-- Condition 2: ARIA (Confounded: Semantic Attribute + Lexical Co-Location) -->
<div class="product-card">
  <h3>SoundFlow Air 3</h3>
  <span class="price">$79.99</span>
  <button aria-label="Add SoundFlow Air 3 to Cart">Add to Cart</button>
</div>
```

In `BASELINE_ABS`, the LLM receives:
```
Heading: SoundFlow Air 3
Text: $79.99
[Button 14] Add to Cart
```
The agent must execute multi-node relational binding, determining that Button 14 belongs to SoundFlow Air 3 based on DOM proximity or document hierarchy.

In `ARIA`, the serializer emits:
```
[Button 14] Add SoundFlow Air 3 to Cart
```
The agent requires zero hierarchical reasoning; it executes a single-node string match: `if "SoundFlow" in button_text -> click(14)`.

### 3.2 Isolating the Confound: Arm BASELINE_REP
To causally isolate semantic attribute parsing from entity co-location, the four-arm protocol introduces `BASELINE_REP`:

```html
<!-- Condition 3: BASELINE_REP (Visible Co-Location, No ARIA) -->
<div class="product-card">
  <h3>SoundFlow Air 3</h3>
  <span class="price">$79.99</span>
  <button>Add SoundFlow Air 3 to Cart</button>
</div>
```

### 3.3 Planned Causal Contrasts

$$\Delta_{\text{Co-Location}} = E[Y \mid \text{BASELINE\_REP}] - E[Y \mid \text{BASELINE\_ABS}]$$
$$\Delta_{\text{ARIA\_Pure}} = E[Y \mid \text{ARIA}] - E[Y \mid \text{BASELINE\_REP}]$$
$$\Delta_{\text{DATA\_CFG}} = E[Y \mid \text{DATA-CFG}] - E[Y \mid \text{BASELINE\_ABS}]$$

- If $\Delta_{\text{Co-Location}} > 0$ and $\Delta_{\text{ARIA\_Pure}} \approx 0$, then previous claims of "semantic markup superiority" were artifacts of lexical co-location.
- Only if $\Delta_{\text{ARIA\_Pure}} > 0$ can researchers defensibly claim that the semantic attribute syntax itself provides an agent advantage.

---

## 4. Intention-to-Treat (ITT) vs. Conditional-on-Delivery

| Trial Status | Handling in ITT | Handling in Conditional-on-Delivery |
|:---|:---|:---|
| **Clean Completed Runs (N=39)** | Included | Included |
| **Transient Cloud 503 Errors (Run 26)** | Successful retry (attempt 4) scored as 1.0; 3 prior aborts cataloged as infrastructure latency | Attempt 4 evaluated; retries penalized in secondary latency metric |
| **Duplicate Completed Runs (Runs 34 & 38)** | Quarantined to maintain balanced block orthogonality ($N=39$) | Evaluated in sensitivity analysis ($N=41$) |
| **Unexecuted Runs (Runs 42–72)** | Censored due to fail-closed budget halt; zero imputation | Excluded from analysis |

---

## 5. Ceiling Effect and Discriminative Power

In the exploratory pilot ($N=39$ primary eligible, $N=41$ sensitivity), task success was $100\%$ ($13/13$) across all three arms. 

### Methodological Consequence:
- When baseline performance is $1.0$, the maximum observable treatment benefit is $\Delta_{\max} = 1.0 - 1.0 = 0.0$.
- The pilot benchmark cannot discriminate between observation conditions.
- Claims of "treatment equivalence" are rejected under the Equivalence Fallacy; high p-values reflect lack of headroom and statistical power ($10.8\%$), not equivalence.
