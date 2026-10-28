# REMEDIATION 11: INDEPENDENT ADVERSARIAL REVIEW REPORT
## Project: The DOM Serialization Gap — Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents
**Date:** 2026-10-26  
**Reviewer Role:** Independent Adversarial Reviewer (External Methodology, Systems & Causal Audit)  
**Verdict:** **DEFENSIBLE AS A SYSTEMS AUDIT PAPER WITH EXPLICIT LIMITATIONS**

---

## 1. Adversarial Reviewer Assessment

As an independent adversarial reviewer, I have rigorously evaluated the claims, code, data ledgers, statistics, and manuscript layout to attempt to falsify the central findings.

### Stress Test 1: Can the serializer pruning findings be falsified?
- **Finding:** In `browser-use 0.13.10`, JSON-LD and container `aria-label` attributes are pruned prior to model observation.
- **Adversarial Challenge:** Could this be an artifact of testing or configuration rather than framework architecture?
- **Forensic Verification:** 
  - Line 18 of `browser_use/dom/serializer/serializer.py` explicitly hardcodes `DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}`. Line 481 returns `None` immediately without traversing children. JSON-LD in `<script type="application/ld+json">` is discarded unconditionally.
  - Lines 1046–1051 gate tag serialization on `node.is_interactive or is_any_scrollable`. A non-interactive `<span>` or `<div>` has opening/closing tags and all attributes bypassed; `_build_attributes_string` is never invoked.
  - A runtime trace on `fixtures/disambiguation_probe_b.html` independently confirmed that `aria-label` on a container span was omitted at Stage 4.
- **Verdict:** **CONFIRMED IMPLEMENTATION MECHANISM.** Falsification failed.

### Stress Test 2: Does the pilot data show that ARIA helps agent performance?
- **Finding:** In the exploratory pilot, all 39 primary eligible runs succeeded ($13/13$ ABS, $13/13$ ARIA, $13/13$ DATA-CFG).
- **Adversarial Challenge:** Can the authors claim ARIA markup provides an advantage to agents?
- **Forensic Verification:**
  - With zero variance across arms ($\Delta = 0.000$), the experimental task battery hit a complete ceiling effect.
  - Claiming that ARIA helps agents is scientifically false. The manuscript correctly refrains from this claim and explicitly reports the ceiling effect.
- **Verdict:** **CLAIM DEFENDED AND HONESTLY BOUNDED.**

### Stress Test 3: Does $p = 1.000$ prove that markup has no effect (The Equivalence Fallacy)?
- **Finding:** Fisher's exact test yields $p = 1.0000$.
- **Adversarial Challenge:** Older drafts claimed this proved baseline and ARIA were equivalent.
- **Forensic Verification:**
  - With $n=13$ per arm, the 95% Newcombe hybrid score interval is $[-0.232, +0.232]$. The data cannot rule out a $20\%$ benefit or a $20\%$ detriment.
  - A formal Two One-Sided Tests (TOST) equivalence test within a $\pm 10\%$ margin fails to reject the non-equivalence null. Establishing equivalence would require $n \ge 275\text{--}360$ runs per arm.
  - The manuscript refactored Section IV and Appendix A to explicitly highlight this fallacy.
- **Verdict:** **DEFECT RESOLVED; STATISTICAL HONESTY RESTORED.**

### Stress Test 4: Are experimental trial counts manipulated?
- **Finding:** Historical mentions of 25, 27, 39, 41, 46, 72, 80, 96, 1080, and 1440.
- **Adversarial Challenge:** Are the authors selectively reporting runs to manufacture a result?
- **Forensic Verification:**
  - All 46 raw JSON traces in `results/3arm_runs/` were independently inspected.
  - Exactly 38 single completed runs exist, 1 recovered retry run (Run 26: 3 transient HTTP 503 aborts + 1 success), and 2 duplicate completed runs (Runs 34 & 38: 2 attempts each).
  - De-duplicating Runs 34 and 38 yields exactly 39 primary eligible units (13 ABS, 13 ARIA, 13 DATA-CFG). Sensitivity analysis evaluates all 41 completed attempts (15 DATA-CFG).
  - 72 was the scheduled count (Runs 42–72 unattempted due to budget ceiling). 96 is the proposed confirmatory schedule. 1,440 is the theoretical TOST sample size.
- **Verdict:** **PROVENANCE 100% RECONCILED AND TAMPER-PROOF.**

---

## 2. Adversarial Reviewer Conclusion

The paper cannot be published as a confirmatory behavioral benchmark because confirmatory live trials remain unexecuted ($N=0$) and the pilot exhibited a ceiling effect. 

However, as an **implementation-level systems audit and measurement study**, the paper makes a rigorous, reproducible, and defensible scientific contribution that exposes critical blind spots in autonomous browser agent observation pipelines.
