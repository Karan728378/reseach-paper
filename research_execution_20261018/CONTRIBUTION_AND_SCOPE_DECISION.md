# CONTRIBUTION AND SCOPE DECISION: SYSTEMS AUDIT VS. BEHAVIORAL EFFICACY (PHASE 5)

**Project:** *The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents*  
**Host Workspace:** `C:\testing\research_execution_20261018`  
**Date (UTC):** 2026-10-27  
**Decision Authority:** Senior Research Lead, Reproducibility Auditor, and Academic Editor  

---

## 1. Evaluation of Candidate Scientific Contributions

We critically evaluate two contrasting contributions to determine which one the existing empirical evidence actually supports:

### Contribution Model A: Version-Pinned Serializer Systems Audit & Preflight Framework
- **Core Claim:** Client-side DOM observation serialization pipelines in autonomous web agent frameworks (specifically `browser-use 0.13.10` and its v0.1.0–v0.13.11 release history) systematically prune, strip, and distort semantic web metadata (Schema.org JSON-LD, developer `data-*`, non-interactive container ARIA) before it reaches the model prompt. Naive benchmark evaluations comparing semantic markup variants are confounded by silent client-side pruning, accessibility tree circularity, geometric heuristics, and visible text solvability.
- **Evidence Base:**
  - 100% verified source code AST inspections mapped to exact lines (`serializer.py` L18/L481, L1046–1051; `views.py` L18).
  - Cryptographically verified SHA-256 digests across 6 official PyPI binary wheels (v0.1.0 to v0.13.11).
  - Concrete retention measurements across 44 atomic target entities and 7 fixtures with exact Clopper-Pearson binomial CIs (`INFORMATION_LOSS_MEASUREMENTS.csv`).
  - Chromium CDP Blink AXTree selector census ($26/26$ leaf controls, 7 heuristic false-positive badge spans).
  - Non-LLM scripted oracle reader proving $p=1.0$ solvability on visible text.
  - Clean-room Monte Carlo power simulations ($B=10\,000$) proving small-sample experiments ($n \le 20$/arm) lack power ($<12\%$).
- **Defensibility Assessment:** **HIGHLY DEFENSIBLE (100% Empirically Supported).** This is a rigorous, unassailable systems contribution to web agent engineering and benchmark reproducibility.

### Contribution Model B: Empirical Behavioral Efficacy of Semantic Web Markup
- **Core Claim:** Augmenting web pages with additive semantic markup (WAI-ARIA or custom `data-*` attributes) improves or alters LLM browser agent transactional success rates, planning efficiency, or execution latency in live production environments.
- **Evidence Base:**
  - Historical cloud pilot ($N=39$ primary eligible runs, $13/13$ per arm on `gemini-flash-lite-latest`).
  - Empirical result: Success rate is identically 100% across all arms ($\hat{\theta} = 0.00$).
  - Power analysis: Statistical power to detect $\Delta=0.20$ is only 7.5% (3-arm) / 11.5% (pooled).
  - Exact 95% Clopper-Pearson CI: $[0.7529, 1.0000]$ (leaving undetected failure rate up to $24.71\%$).
- **Defensibility Assessment:** **NOT DEFENSIBLE TODAY.** The exploratory pilot suffered from an acute measurement ceiling effect because standard tasks were completely solvable from rendered typography alone. No confirmatory live behavioral trials have been executed. Claiming behavioral efficacy or behavioral equivalence from this pilot would be a serious methodological error (the Equivalence Fallacy).

---

## 2. Contextualization & Boundaries of the Scripted Oracle Solvability Proof

The discovery that standard TechMart benchmark routes were 100% solvable ($p=1.0$) from visible rendered text alone is a pivotal diagnostic finding that must be precisely bounded:

### 2.1 Supported Solvability Scope
- **Evaluated Routes:** Standard TechMart e-commerce routes `#home`, `#category/audio`, `#product/wh-001`, `#cart`, and `#checkout`.
- **Evaluated Tasks:** Tasks T1 through T5 (adding lowest-price item, searching named product, selecting rating, form filling, cart clearing).
- **Oracle Mechanism:** A deterministic Python string parser that searches Stage 4 serialized strings for the exact product names, prices, and button labels present in the task prompt.
- **Result:** In all five standard tasks, rendered typography uniquely identifies the target product card and its corresponding action button without ambiguous SKU collisions.
- **Significance:** This proves mathematically why the exploratory pilot achieved 13/13 success in every arm: the LLM never needed semantic markup to solve these tasks because visible typography provided complete information.

### 2.2 Prohibited Generalization (What This Does NOT Prove)
- **Visible Text Is NOT Universally Sufficient:** This finding does **not** prove that visible text is sufficient for all web tasks or all websites.
- **Counter-Proof in Fixtures:** When we evaluated Disambiguation Probe B (where two identical products share the visible name "Refurbished Monitor" and differ only in container ARIA markup), the task is mathematically **unsolvable** from visible text ($p=0.5$, random guessing), and container ARIA stripping in the serializer prevents the agent from resolving the ambiguity.
- **Manuscript Correction:** Any claim in previous drafts that "visible typography alone was proven fully sufficient" is formally retracted. The finding is presented strictly as an explanation for the pilot's ceiling effect on this specific benchmark battery.

---

## 3. Supported, Weakened, and Unsupported Claims Matrix

| Claim Category | Specific Proposition | Prior Draft Status | Current Audited Status | Scientific Justification |
| :--- | :--- | :---: | :---: | :--- |
| **Systems Fact** | Schema.org JSON-LD is eliminated at Stage 2. | Claimed attribute whitelist caused loss. | **VERIFIED & PROVEN** | Mapped to `DISABLED_ELEMENTS = {'style','script',...}` at `serializer.py` L18/L481; verified across 6 wheels. |
| **Systems Fact** | Container ARIA attributes on `<span>` and `<div>` are stripped. | Claimed generic roles prohibit naming. | **VERIFIED & PROVEN** | Mapped to interactivity gate at `serializer.py` L1046–1051; verified on W3C WAI-ARIA 1.2 landmark containers. |
| **Systems Fact** | Developer `data-*` attributes are omitted by default. | Claimed all `data-*` omitted. | **CALIBRATED & PROVEN** | `DEFAULT_INCLUDE_ATTRIBUTES` in `views.py` retains framework state but omits developer custom attributes. |
| **Systems Fact** | AXTree correspondence is partially circular. | Presented as independent validation. | **DISCLOSED & PROVEN** | `ClickableElementDetector` directly inspects `node.ax_node.role` via CDP `Accessibility.getFullAXTree`. |
| **Systems Fact** | $10\text{--}50$\,px icon heuristic creates false positives. | Unacknowledged. | **DISCLOSED & PROVEN** | Heuristic misclassifies 7 static "In Stock" text badge spans ($48.6 \times 15$\,px) as interactive buttons. |
| **Methodology** | Small-sample web agent experiments ($n \le 20$/arm) lack power. | Preliminary power cited ($10.8\%$, $49.6\%$). | **VERIFIED & REPRODUCED** | Clean-room Monte Carlo ($B=10\,000$) proves 7.5% (3-arm) and 11.5% (pooled) power for $\Delta=0.20$. |
| **Behavioral** | Semantic markup improves agent performance. | Hypothesized. | **UNSUPPORTED / UNTESTED** | No confirmatory behavioral trials executed; existing pilot confounded by ceiling effect. |
| **Behavioral** | Visible typography is proven sufficient for agent reasoning. | Claimed. | **RETRACTED** | Proved to be a benchmark ceiling effect; disproven by Disambiguation Probe B. |

---

## 4. Requirements for Future Confirmatory Behavioral Research

To transition from this systems audit to a defensible behavioral efficacy study in future work, researchers must satisfy five strict preflight requirements:

1. **Pre-Register Hard Tasks (No Ceiling):** Design benchmark tasks where options share identical visible typography and disambiguation requires inspecting target metadata.
2. **Stage 5 Prompt Interception:** Programmatically assert via regex that target metadata survived client-side serialization and exists in the model prompt buffer before dispatching API calls.
3. **Decouple Content Placement from Channel:** Ensure action button labels remain identical across ablation conditions to eliminate the Action-Label Co-Location Confound.
4. **State-Asserted DOM Verifiers:** Evaluate task outcomes exclusively through post-run browser state assertions (e.g., `localStorage.cart`), never via LLM conversational self-reporting.
5. **Power for $N \ge 300$ Trials:** Execute at least $n=97\text{--}125$ trials per arm ($N \ge 291\text{--}375$) to achieve 80% statistical power for moderate effects ($\Delta=0.20$).

---

## 5. Formal Scope Resolution

**The manuscript will strictly remain a Version-Pinned Systems Audit and Methodological Preflight Paper.** 

Under the user-directed offline completion mandate ($0.00 spend), zero live commercial API calls have been or will be made. The paper makes zero behavioral efficacy claims, reports the pilot transparently as a ceiling observation, and provides an unassailable systems baseline for the autonomous web agent community.
