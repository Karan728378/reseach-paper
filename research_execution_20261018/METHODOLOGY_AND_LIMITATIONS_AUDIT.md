# Experimental Methodology, Confounds & Threats to Validity Audit

**Date:** 2026-10-25  
**Auditor:** Independent Systems & Methodology Auditor  
**Project:** *The DOM Serialization Gap in Autonomous Browser Agents*  
**Workspace:** `C:\testing\research_execution_20261018`  

---

## Executive Summary

This audit assesses the experimental validity of the research design, isolates potential confounding variables, and provides a comprehensive analysis of threats to validity. We examine the action-label co-location confound, document the ceiling effect observed in the Phase 1 pilot, and define explicit boundaries for generalizability.

---

## 1. Experimental Confounds & Mitigations

### 1.1 The Action-Label Co-Location Confound
- **The Vulnerability in Prior Literature:**  
  When authors attempt to evaluate whether ARIA accessibility markup aids web agents, stimulus markup often augments action triggers with full target entity names:
  ```html
  <!-- Confounded Stimulus -->
  <button class="btn-add-cart" aria-label="Add SoundFlow Air 3 to cart">Add to Cart</button>
  ```
- **Construct Contamination:**  
  In this setup, an agent task instructing *"Add SoundFlow Air 3 to cart"* no longer requires the agent to understand product cards, correlate prices, or resolve hierarchical parent-child relationships. The agent simply scans the serialized text buffer for the exact string `"SoundFlow Air 3"` and clicks the button where that string appears. Any measured performance delta reflects **target-string co-location and button disambiguation**, not generalized semantic comprehension.
- **Audited Code Fix (`shared/app-core.js:Line 243`):**  
  ```javascript
  var addBtn = document.createElement('button');
  addBtn.className = 'btn-add-cart';
  if (F.aria) addBtn.setAttribute('aria-label', 'Add item to cart');
  if (F.dataAttrs) {
    addBtn.setAttribute('data-action', 'add-to-cart');
    addBtn.setAttribute('data-product-id', product.sku);
  }
  ```
- **Verification:**  
  The button label is standardized to `"Add item to cart"` across all variants. The target entity name is completely removed from the action trigger in `v2-aria`. In `test_treatment_leakage_and_integrity.py`, line 42, automated tests assert:
  `self.assertNotIn("SoundFlow", button_aria_label)`  
  Ensuring zero target-name leakage.

### 1.2 Channel Separation & Information Leakage Audit
We audited whether any side channel could leak the target answer to the agent:
1. **Rendered Typography:** Product cards display the product title and price in plain text (`card.appendChild(title)`). This information is intentionally identical across all arms (\textsc{ABS}, \textsc{ARIA}, \textsc{DATA-CFG}).
2. **URL and Title:** The page title (`"TechMart - Products"`) and hash routes (`"#home"`, `"#cart"`) are identical across variants.
3. **Structured Data:** In `v1-jsonld`, `<script type="application/ld+json">` is pruned at Stage 4 (`DISABLED_ELEMENTS`), preventing prompt leakage.
4. **Conclusion:** Treatment delivery is pure and de-confounded; observed differences in the prompt buffer reflect only the intended serialized markup manipulation.

---

## 2. Experimental Rigor: Ceiling Effect in Phase 1

### 2.1 The 41-Trial Pilot Outcome
Across 41 unique completed live trials using `gemini-3.1-flash-lite`, the success rate was:
- \textsc{ABS} (Control): **13 / 13 (100%)**
- \textsc{ARIA} (Semantic): **13 / 13 (100%)**
- \textsc{DATA-CFG} (Custom Attributes): **15 / 15 (100%)**

### 2.2 Forensic Diagnosis of the Ceiling Effect
1. **Task Complexity:** Tasks T1–T6 in the initial TechMart catalog featured clear search queries and clean layout hierarchy.
2. **Model Baseline Capability:** `gemini-3.1-flash-lite` possessed sufficient reasoning to locate and purchase items using plain visible typography alone.
3. **Statistical Consequence:** When baseline performance is $1.0$, the observed risk difference is identically zero ($\hat{\theta} = 0.0$). The task battery lacked sufficient difficulty to discriminate between representations.
4. **Reporting Invariant:** This pilot **CANNOT** be presented as a confirmatory benchmark or as proof that metadata is ineffective. It must be reported strictly as an **exploratory pilot demonstrating a ceiling effect**.

---

## 3. Comprehensive Threats to Validity

### 3.1 Construct Validity
- **Observation Space vs. Multimodal Vision:** Audited exclusively under text-only observation (`use_vision=False`). Multimodal agents utilizing screenshot inputs can observe visual typography directly, bypassing DOM serializer pruning.
- **Non-Interactive ARIA Intent:** W3C WAI-ARIA was designed for assistive technologies (screen readers), not LLM scrapers. Screen readers utilize platform accessibility APIs (e.g., UI Automation, NSAccessibility), which query Chromium's AXTree directly. The loss of non-interactive ARIA semantics occurs inside the agent library's custom DOM serializer, not within the browser itself.

### 3.2 Internal Validity
- **Watchdog Truncation in Local Models:** As demonstrated in local `qwen3:4b` runs, hybrid CPU/GPU hardware requires 160–213 seconds for prompt ingestion on contexts $>3,200$ tokens. If a fixed 180-second step watchdog is enforced, runs truncate due to hardware latency rather than reasoning failure.
- **Provider Infrastructure Failures:** In the cloud pilot, Run 26 encountered 3 transient `503 UNAVAILABLE` errors before succeeding. Infrastructure aborts must be tracked separately from agent task failures.

### 3.3 External Validity & Generalizability
- **Single-Framework Scope:** All static AST code audits and serializer measurements were performed on `browser-use 0.13.10`. Other agent frameworks (e.g., BrowserGym, Crawl4AI, Stagehand, Skyvern) employ different DOM simplification heuristics.
- **Synthetic Fixture Scope:** Measurements were obtained on a controlled e-commerce benchmark environment. While this isolates markup channels from visual occlusions, wild commercial websites contain third-party ad tags, complex shadow DOMs, and obfuscated CSS class names that may alter serialization.
- **Route-Specific Node Correspondence:** The $79.4\%$ ($27/34$) Blink node correspondence was measured on route `#home`. Routes with extensive dynamic forms or complex tables may exhibit different correspondence ratios.

---
*Report certified by Independent Systems & Methodology Auditor.*
