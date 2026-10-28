# METHODS AND CAUSAL IDENTIFICATION AUDIT
## Project: The DOM Serialization Gap — Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents
**Date:** 2026-10-26  
**Auditor:** Research Methodology & Causal Inference Working Group  
**Environment:** Python 3.11 (`C:\testing\.venv311\Scripts\python.exe`)

---

## 1. Executive Summary

Autonomous browser agent benchmarks frequently conflate observation pipeline mechanics with agent cognitive performance, resulting in severe threats to causal validity. This audit evaluates the causal identification strategy, experimental design, potential confounds, and estimand definitions for the DOM Serialization Gap project.

### Core Methodological Insights:
1. **The Action-Label Co-Location Confound:**
   - In standard accessible web design, `aria-label` attributes placed on interactive controls often include the full descriptive entity name (e.g., `<button aria-label="Add Wireless Noise-Cancelling Headphones to Cart">Add</button>`).
   - In contrast, unaugmented baseline markup typically isolates the entity name in a sibling heading (`<h3>Wireless Noise-Cancelling Headphones</h3>`) while the button contains generic text (`<button>Add</button>`).
   - An agent in the ARIA condition can identify the target in a single lexical pattern match on the button, whereas in the baseline condition it must perform multi-node relational binding.
   - Any observed performance gain in ARIA may therefore reflect **entity-name co-location** rather than the semantic accessibility of the markup.
2. **Treatment Isolation Across Arms:**
   - The proposed four-arm confirmatory design (`BASELINE_ABS`, `BASELINE_REP`, `ARIA`, `DATA-CFG`) controls for this confound by introducing `BASELINE_REP`, where the entity name is repeated in visible inner text, isolating the semantic attribute mechanism from lexical co-location.
3. **Observation-Pipeline Reachability vs. Behavioral Claims:**
   - Direct inspection of serializer code (`browser_use/dom/serializer/serializer.py`) establishes that certain metadata (JSON-LD, container `aria-label`, custom `data-*` attributes) are pruned at Stage 4.
   - However, demonstrating that metadata is pruned from the observation does NOT prove that supplying this metadata improves agent success rates. Systems audits and behavioral experiments must remain cleanly separated.
4. **Intention-to-Treat (ITT) vs. Per-Protocol / Conditional-on-Delivery:**
   - Transient infrastructure errors (e.g., Run 26 HTTP 503 errors from the remote API) must be distinguished from task execution failures.
   - Run 26 was successfully recovered after transient 503 backoff; Runs 34 and 38 (duplicate runs) were quarantined in primary ITT analysis.

---

## 2. The Action-Label Co-Location Confound

### 2.1 Mechanism of the Confound
When designing experimental treatments to test whether "semantic markup" aids LLM browser agents, naive implementations introduce an unmeasured confound:

```html
<!-- Baseline (ABS): Relational Binding Required -->
<div class="product-card">
  <h3>Sony WH-1000XM5</h3>
  <p>$399.99</p>
  <button>Add to Cart</button>
</div>

<!-- ARIA Arm (Confounded with Co-Location): Single-Node Match -->
<div class="product-card">
  <h3>Sony WH-1000XM5</h3>
  <p>$399.99</p>
  <button aria-label="Add Sony WH-1000XM5 to Cart">Add to Cart</button>
</div>
```

In the ARIA condition, the LLM prompt contains:
`[Button 12] Add Sony WH-1000XM5 to Cart`
The LLM can select Button 12 via a simple token matching rule: `"Sony" in button_text`.

In the Baseline condition, the LLM prompt contains:
`Heading: Sony WH-1000XM5`
`Text: $399.99`
`[Button 12] Add to Cart`
The LLM must infer spatial/DOM hierarchy proximity to connect Button 12 with the Sony heading.

### 2.2 Proposed Experimental Control: Arm BASELINE_REP
To causally isolate the effect of the `aria-label` attribute from the text co-location, the four-arm protocol introduces a repeated visible baseline:

```html
<!-- Baseline Repeated (REP): Visible Co-Location without ARIA -->
<div class="product-card">
  <h3>Sony WH-1000XM5</h3>
  <p>$399.99</p>
  <button>Add Sony WH-1000XM5 to Cart</button>
</div>
```

By contrasting:
- **ARIA vs. BASELINE_REP:** Tests the specific contribution of the `aria-label` attribute syntax, holding lexical co-location constant.
- **BASELINE_REP vs. BASELINE_ABS:** Measures the pure effect of lexical co-location without semantic markup.

---

## 3. Experimental Design and Blocking Architecture

### 3.1 Randomized Complete Block Design (RCBD)
To control for temporal drift, remote API latency, and task difficulty heterogeneity:
- **Blocks:** Temporal execution epochs consisting of complete sets of treatments.
- **Randomization:** Within each block, treatment assignments and task order are pseudo-randomized using a fixed seed (`seed=42`).
- **Cluster Unit:** The experimental unit is the individual task trial $(i, j, k)$ for block $i$, treatment $j$, and task construct $k$.

### 3.2 Task Construct Matrix
The experimental battery spans 6 task archetypes designed to test distinct cognitive demands:

| Task ID | Task Construct | Target Challenge | Verifier Ground Truth Criterion |
|:---:|:---|:---|:---|
| **T1** | Direct Target Search | Simple lookup & cart addition | Exact item in cart; score = 1.0 |
| **T2** | Filter & Facet Navigation | Multi-step state mutation | Filter applied, correct item added; score = 1.0 |
| **T3** | Attribute-Constrained Selection | Budget / spec constraints | Selected item satisfies constraints; score = 1.0 |
| **T4** | Multi-Item Comparison | Cross-node comparison | Correct lowest/highest spec added; score = 1.0 |
| **T5** | Adversarial Disambiguation | Near-identical distractors | Correct SKU disambiguated via metadata; score = 1.0 |
| **T6** | Absent-Fact Probe | Hallucination / refusal test | Explicit refusal statement emitted; score = 1.0 |

---

## 4. Verifier Scoring and Refusal Integrity

### 4.1 Strict Objective Verification
All task outcomes are evaluated by deterministic offline verifier scripts inspecting the live browser DOM state and agent action history:
- Cart contents are verified via DOM element inspection on `#cart`.
- Submissions are evaluated against ground truth JSON specifications (`task_specifications.json`).
- Agent self-reports ("I have completed the task") are never accepted without state verification.

### 4.2 Task T6 Scoring Protocol
Task T6 assesses model behavior when the requested fact is absent from the page:
- **Success (Score 1.0):** Model explicitly declares that the item or attribute is absent/unavailable.
- **Failure (Score 0.0):** Model hallucinates a price, selects an unrelated product, or executes an arbitrary click action.
- **Refusal Guard:** The verifier requires semantic pattern matching for genuine abstention phrases (e.g., `"not found"`, `"not available"`, `"cannot find"`) while rejecting generic runner error crashes.

---

## 5. Intention-to-Treat (ITT) vs. Conditional-on-Delivery Analysis

| Run Category | Count | Handling in ITT Analysis | Handling in Conditional-on-Delivery |
|:---|:---:|:---|:---|
| **Completed Clean Trials** | 39 | Included in primary analysis. | Included in primary analysis. |
| **Recovered HTTP 503 Retries (Run 26)** | 1 | Attempt 4 succeeded; counted as success. | Evaluated with latency / retry penalty. |
| **Duplicate Runs (Runs 34 & 38)** | 2 | Quarantined to preserve balanced design ($N=39$). | Evaluated in sensitivity analysis ($N=41$). |
| **Unexecuted Runs (Runs 42–72)** | 31 | Censored due to budget gate halt; not imputed. | Excluded from completed trial analysis. |

---

## 6. Scientific Generalization Boundaries

1. **Single SPA Fixture:** All empirical findings derive from a single controlled single-page e-commerce fixture (`http://127.0.0.1:8094/`). Generalization to heterogeneous web ecosystems requires testing on multi-domain benchmarks (e.g., WebArena, VisualWebArena).
2. **Framework Version Scope:** Architectural pruning findings are verified for `browser-use 0.13.10`. Newer or alternative frameworks (e.g., Playwright raw, Stagehand, Agent-E) may utilize different DOM serialization policies.
3. **Model Checkpoint:** Cloud runs targeted endpoint alias `gemini-flash-lite-latest`. The underlying physical model weights are maintained remotely by Google and are subject to server-side updates.
