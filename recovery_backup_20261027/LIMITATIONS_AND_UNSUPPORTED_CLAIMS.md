# LIMITATIONS AND UNSUPPORTED CLAIMS REGISTER
## Project: The DOM Serialization Gap — Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents
**Date:** 2026-10-26  
**Auditor:** Research Integrity & Scientific Methodology Committee  
**Status:** Permanent Audit Document — Preserves Scientific Honesty and Bounded Scope

---

## 1. Executive Statement of Research Integrity

In accordance with strict scientific integrity principles:
- **No Results Fabricated:** Zero live-model trials, trial counts, confidence intervals, p-values, or test results have been fabricated.
- **No Overclaiming:** Exploratory pilot trials are never described as confirmatory findings.
- **Fail-Closed Safety Gate:** Budget and live-execution safety gates remain strictly locked. No paid API spend was incurred during remediation.
- **Negative and Null Findings Preserved:** The exploratory ceiling effect and lack of behavioral discrimination are reported transparently.

---

## 2. Bounded Scientific Scope and Accepted Limitations

| Limitation ID | Category | Verified Constraint | Allowed Scientific Claim | Forbidden Overclaim |
|:---|:---|:---|:---|:---|
| **LIM-01** | Observation Pipeline Stage | Serializer inspection is verified at Stage 4 (`dom_state.llm_representation()`). Full Stage 5 assembled prompt buffer was not intercepted during the pilot. | "Stage-4 serialized observation prunes non-interactive container attributes and script/meta elements." | "The LLM never saw the metadata at Stage 5." |
| **LIM-02** | Framework Specificity | Implementation evidence is verified exclusively on `browser-use 0.13.10`. | "In `browser-use 0.13.10`, tag serialization is gated on interactivity at lines 1046–1051." | "All autonomous browser agents omit container attributes." |
| **LIM-03** | Web Fixture Scope | Empirical measurements are conducted on a single synthetic e-commerce SPA fixture (`http://127.0.0.1:8094/`). | "Within the controlled e-commerce SPA fixture, 27/34 selector targets correspond to interactive controls." | "Across the web, 79.4% of elements correspond to accessibility nodes." |
| **LIM-04** | Pilot Ceiling Effect | Primary pilot sample ($N=39$ eligible, $N=41$ sensitivity) exhibited $100\%$ task success across ABS, ARIA, and DATA-CFG. | "In the exploratory pilot, all arms achieved 100% success, precluding behavioral discrimination due to a ceiling effect." | "ARIA semantic markup significantly improves agent success rates." |
| **LIM-05** | Fallacy of Equivalence | Fisher's exact test yielded $p = 1.000$ and $\Delta = 0.000$ ($95\%$ Newcombe CI $[-0.232, +0.232]$). | "The observed difference was $\Delta = 0.000$, with confidence intervals spanning $[-23.2\%, +23.2\%]$; the design is underpowered to detect or reject small effects." | "We prove that semantic markup has no effect on agent performance." |
| **LIM-06** | Unexecuted Confirmatory Study | The proposed 4-arm 96-trial confirmatory study has **0 executed live runs**. | "We propose a pre-registered 4-arm confirmatory design ($N=96$) to resolve the Action-Label Co-Location Confound." | "Our confirmatory experiments prove the effectiveness of BASELINE_REP." |
| **LIM-07** | Endpoint Alias & Checkpoint | Remote cloud experiments utilized API alias `gemini-flash-lite-latest` (`gemini-3.1-flash-lite`). | "Experiments used Google Gemini API endpoint `gemini-flash-lite-latest` on 2026-10-18." | "Experiments evaluated Gemini 1.5 Flash checkpoint 002." |
| **LIM-08** | Physical Hardware Environment | Local machine is ASUS TUF Gaming A15 (AMD Ryzen 7 7435HS, 16 GB RAM, RTX 2050 4 GB GPU). Cloud experiments ran remotely; local Ollama Qwen pilot ran on CPU. | "Local execution environment: AMD Ryzen 7 7435HS, 16 GB RAM, NVIDIA RTX 2050 (cloud trials ran via remote API)." | "Cloud trials utilized local GPU acceleration." |
| **LIM-09** | Action-Label Co-Location Confound | Standard ARIA markup places entity names directly on buttons, creating a potential confound. | "The observed ARIA condition introduces potential entity-name co-location confounds." | "ARIA markup is an orthogonal semantic manipulation." |
| **LIM-10** | Quarantined Duplicate Runs | Runs 34 and 38 experienced runner race conditions resulting in 2 completed attempts each. | "Primary analysis excludes 2 duplicate attempts ($N=39$); sensitivity analysis includes them ($N=41$)." | "All 41 runs were unique scheduled units without duplication." |

---

## 3. Explicitly Disavowed and Unsupported Claims

The following claims have been audited and permanently struck from all manuscripts, presentations, and submissions:

1. ❌ **"Semantic markup guarantees a 100% success rate in autonomous agents."**  
   *Correction:* All arms (including baseline without markup) achieved 100% success due to task ceiling effects.
2. ❌ **"We evaluated 1,440 experimental runs."**  
   *Correction:* 1,440 represents the theoretical sample size requirement for a 4-arm TOST equivalence trial with a $\pm 10\%$ margin. Zero confirmatory runs have been executed.
3. ❌ **"The serializer bottleneck prevents any LLM from seeing DOM metadata."**  
   *Correction:* Serializer pruning occurs at Stage 4 of `browser-use 0.13.10`. Multimodal vision agents or custom serialization pipelines can bypass this bottleneck.
4. ❌ **"Our findings prove that browser-use has a critical architectural bug."**  
   *Correction:* Pruning non-interactive tags is an intentional token-conservation heuristic, but it produces unintended semantic information loss when metadata is placed on container elements.
5. ❌ **"Our literature review proves no prior work has studied DOM serialization."**  
   *Correction:* Related work has examined DOM distillation and accessibility trees (e.g., Mind2Web, WebArena); this study provides specific empirical measurements of token pruning and attribute whitelisting in `browser-use 0.13.10`.

---

## 4. Current Defensible Scientific Contribution

The scientifically defensible contribution of this work is:
> **An implementation-level systems and measurement audit of the observation pipeline in `browser-use 0.13.10`, demonstrating that standard token-pruning heuristics discard JSON-LD metadata, non-interactive container `aria-label` attributes, and custom `data-*` attributes prior to model observation, accompanied by an exploratory pilot benchmark establishing task ceiling effects and identifying the Action-Label Co-Location Confound.**
