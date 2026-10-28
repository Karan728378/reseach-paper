# REVISION EVIDENCE AUDIT: THE DOM SERIALIZATION GAP
**Document Version:** 1.0 (Master Revision Evidence Inventory)  
**Date:** October 25, 2026  
**Auditor:** Independent Research Auditor & Systems Methodology Reviewer  
**Workspace:** `C:\testing\research_execution_20261018\`  
**Python Environment:** `C:\testing\.venv311\Scripts\python.exe` (Python 3.11.9)  

---

## 1. Provenance and Software Environment

| Component | Verified Value | Evidence Source | Status |
| :--- | :--- | :--- | :--- |
| **Package Name** | `browser-use` | `C:\testing\.venv311\Lib\site-packages\browser_use-0.13.10.dist-info\METADATA` | VERIFIED |
| **Package Version** | `0.13.10` | `dist-info/METADATA: Version: 0.13.10`, `INSTALLER: pip` | VERIFIED |
| **Installation Provenance** | PyPI standard wheel distribution | `dist-info/INSTALLER: pip`; no `direct_url.json` (unpinned commit hash) | VERIFIED |
| **Package Author** | Gregor Zunic | `dist-info/METADATA: Author: Gregor Zunic` | VERIFIED |
| **Repository URL** | `https://github.com/browser-use/browser-use` | `dist-info/METADATA: Project-URL: Repository` | VERIFIED |
| **Python Runtime** | Python 3.11.9 (Windows 11) | `sys.version`, `sys.executable` | VERIFIED |
| **CDP Automation Layer** | `cdp-use 1.4.5` | `C:\testing\.venv311\Lib\site-packages\cdp_use` | VERIFIED |
| **Playwright Status** | Not installed (`ModuleNotFoundError`) | Documented in `compare_accessibility_tree.py:L53--L59` | VERIFIED |

---

## 2. Serializer Source Code Properties (Static AST Facts)

All static filtering rules were verified directly in the installed source code at `C:\testing\.venv311\Lib\site-packages\browser_use\`:

### 2.1 Script and Meta Exclusion Rule
- **Source File:** `browser_use/dom/serializer/serializer.py`
- **Line 18:** `DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}`
- **Lines 481–482 (`_create_simplified_tree`):**
  ```python
  if node.node_name.lower() in DISABLED_ELEMENTS:
      return None
  ```
- **Factual Consequence:** Any element matching `DISABLED_ELEMENTS` is immediately pruned from the observation graph; its subtree and attributes are never traversed. Schema.org JSON-LD structured data (`<script type="application/ld+json">`) and custom metadata tags (`<meta name="...">`) suffer deterministic exclusion ($0\%$ reachability to the observation buffer).

### 2.2 Non-Interactive Element Tag Stripping
- **Source File:** `browser_use/dom/serializer/serializer.py`
- **Lines 1046–1058 (`_serialize_node`):**
  ```python
  is_any_scrollable = node.original_node.is_actually_scrollable or node.original_node.is_scrollable
  if (
      node.is_interactive
      or is_any_scrollable
      or node.original_node.tag_name.upper() == 'IFRAME'
      or node.original_node.tag_name.upper() == 'FRAME'
  ):
      next_depth += 1
      attributes_html_str = DOMTreeSerializer._build_attributes_string(
          node.original_node, include_attributes, text_content
      )
  ```
- **Factual Consequence:** If an element is not interactive (not clickable, not scrollable, and not a frame):
  - No HTML tag is output for that element.
  - The serializer continues to child text nodes, emitting only raw strings.
  - All attributes on non-interactive elements (`aria-label`, `role`, `data-*`, `id`) are discarded.

### 2.3 Attribute Whitelisting Rule
- **Source File:** `browser_use/dom/views.py` (Lines 18–46)
- **`DEFAULT_INCLUDE_ATTRIBUTES`:**
  `['title', 'type', 'checked', 'id', 'name', 'role', 'value', 'placeholder', 'data-date-format', 'alt', 'aria-label', 'aria-expanded', 'data-state', 'aria-checked', 'aria-valuemin', 'aria-valuemax', 'aria-valuenow', 'aria-placeholder', 'pattern', 'min', 'max', 'minlength', 'maxlength', 'step', 'accept']`
- **Filtering Logic (`serializer.py:L1211--L1215`):**
  ```python
  attributes_to_include.update(
      {
          key: str(value).strip()
          for key, value in node.attributes.items()
          if key in include_attributes and str(value).strip() != ''
      }
  )
  ```
- **Factual Consequence:** Developer custom attributes (`data-action`, `data-product-id`, `data-sku`, `data-amount`) are omitted from `DEFAULT_INCLUDE_ATTRIBUTES`. They can reach the observation buffer only on interactive elements when `include_attributes` is explicitly overridden by extended runner configurations (`EXTENDED_ATTRIBUTES`).

---

## 3. Dynamic Reachability and Accessibility Audit Inventory

### 3.1 Multi-Stage Observation Retention Tracing
- **Script:** `audit_metadata_reachability.py`
- **Machine Output:** `serialization_audit_metrics.json` (5,466 bytes)
- **Scope:** 4 website variants (`v0-baseline`, `v1-jsonld`, `v2-aria`, `v3-data-attrs`) and 1 edge-case fixture (`fixtures/edge_cases.html`). Headless Chrome DevTools Protocol interception via `MockChatModel`.
- **Verified Findings:**
  1. `JSON-LD`: $0\%$ reachability across all variants (pruned by `DISABLED_ELEMENTS`).
  2. `Button WAI-ARIA`: $100\%$ reachability on interactive `<button>` elements (retained by whitelist).
  3. `Non-Interactive ARIA`: $0\%$ reachability on `<span>` and `<div>` elements (tags stripped, attributes dropped).
  4. `Custom data-* (Default)`: $0\%$ reachability (omitted from default whitelist).
  5. `Custom data-* (Extended)`: Delivered on interactive elements, but $0\%$ reachability on non-interactive elements.
  6. `Temporal <meta>`: $0\%$ reachability (pruned by `DISABLED_ELEMENTS`).
  7. `Temporal <time>`: Tag stripped, but inner visible text (`September 1, 2026`) is emitted.

### 3.2 Native Chromium AXTree vs. Serializer Correspondence
- **Script:** `compare_accessibility_tree.py`
- **Machine Output:** `accessibility_tree_comparison.json` (22,978 bytes)
- **Protocol:** CDP `Accessibility.getFullAXTree` vs. `browser-use 0.13.10` `dom_state.selector_map`.
- **Evaluated Route:** `variants/v2-aria/index.html#home`.
- **Raw Measurements:**
  - Total Blink AXNodes constructed: 336.
  - AXNodes with `backendDOMNodeId`: 256.
  - Interactive elements identified in `selector_map`: 34.
  - Interactive elements matching an AXNode: Exactly 27 of 34 ($79.4\%$).
- **Forensic Breakdown of the 7 Unmatched Elements:**
  The 7 unmatched elements are stock badge spans (`<span class="product-stock in-stock">In Stock</span>`, selector indices 69, 84, 99, 114, 129, 144, 159) across the first 7 product cards. Tracing their inclusion through the source code reveals they were classified as interactive by `ClickableElementDetector.is_interactive` (`clickable_elements.py:228-240`), which flags any element with a `class` attribute whose layout bounds satisfy $10 \le \text{width} \le 50$ and $10 \le \text{height} \le 50$ as an interactive icon.
  - Measured layout bounding box for each "In Stock" badge: exactly **$48.625\text{px} \times 15.0\text{px}$** (falls within heuristic window).
  - Measured layout bounding box for 8th card "Out of Stock" badge: **$74.766\text{px} \times 15.0\text{px}$** (exceeds 50px threshold, correctly classified non-interactive).
  - Chromium Blink's native `AXObjectCache` treats static inline text spans as non-interactive, flattening them into parent card text runs with `ignored: true` without discrete `backendDOMNodeId` objects.
- **Denominator Legitimacy & Dual-Estimand Analysis:**
  - **Framework Operational Census ($n=34$):** All 34 elements legitimately belong in the framework's interactive denominator because `browser-use` indexes all 34 and exposes them to the LLM prompt as actionable targets ($27/34 = 79.41\%$).
  - **Semantic Interactivity Baseline ($n=27$):** From a ground-truth web semantics perspective, the 7 badges are false positives generated by heuristic size thresholds. The page contains exactly 27 genuine interactive controls (9 links, 16 buttons, 1 input, 1 form). Exactly **$27 / 27$ ($100.0\%$)** of true interactive controls match Chromium's AXTree.
  - The Wilson 95% CI ($[63.2\%, 89.7\%]$) applies under superpopulation uncertainty for similar template layouts, while $27/34$ is the exact descriptive census for route `#home`.

---

## 4. Empirical Cloud Pilot Inventory

- **Runner Script:** `protocol_v3_runner.py`
- **Output Files:** `results/v3_3arm_summary.csv` (44 rows), `results/v3_3arm_summary_raw.csv` (46 rows)
- **Model:** `gemini-3.1-flash-lite` (free-tier locked, `use_vision=False`).
- **Complete Trial Breakdown:**
  - `v3_3arm_summary.csv` contains 44 total attempt records.
  - 3 records (rows 25, 26, 27) represent transient infrastructure aborts on Run 26 (Task T6, Arm ABS) due to `503 UNAVAILABLE` ("This model is currently experiencing high demand...").
  - The 4th attempt succeeded on Run 26 at 02:36:19.
  - Excluding the 3 aborts, there are **exactly 41 completed runs**:
    - \textsc{ABS} (Unaugmented Baseline): 13 / 13 ($100.0\%$)
    - \textsc{ARIA} (Semantic Accessibility): 13 / 13 ($100.0\%$)
    - \textsc{DATA-CFG} (Developer Custom Attributes): 15 / 15 ($100.0\%$)
    - Completed Total: $41 / 41$ ($100.0\%$).
- **Verified Scientific Interpretation:**
  - Task success was independently asserted via programmatic DOM verifiers (`window.__cart__`).
  - Because the control arm achieved $13/13$ ($100\%$), the risk difference across all treatments was identically zero ($\hat{\theta} = 0.0$).
  - **Empirical Ceiling Effect:** The pilot diagnosed a ceiling effect. The baseline tasks were too simple to discriminate between markup representations under Gemini 3.1 Flash Lite. This pilot establishes that unaugmented visible text was sufficient for simple tasks; it **does not** prove that semantic markup is useless or that representations are equivalent.

---

## 5. Local Qwen Hardware Diagnostic Inventory

- **Runner Script:** `local_qwen_smoke_runner.py`
- **Output File:** `results/local_llama_summary.csv` (5 records)
- **Hardware:** Hybrid CPU/GPU (NVIDIA GPU with 4 GB VRAM, offloading 34% of layers to CPU).
- **Target Model:** Local quantized `qwen3:4b` via Ollama.
- **Telemetry Records:**
  1. `qwen3_smoke_001`: Duration 3.34s, 0 steps. Failure: Pydantic schema validation (`max_history_items <= 5`).
  2. `qwen3_smoke_002`: Duration 1013.09s, 2 steps. Success: True (1.0). Step 2 clicked button; Step 3 hung until HTTP read timeout due to missing per-step outer watchdog.
  3. `qwen3_smoke_003`: Duration 288.61s, 2 steps. Success: True (1.0). Step 1 evaluation (102.9s); Step 2 breached 180s watchdog ceiling during prompt evaluation (>3,200 tokens).
  4. `qwen3_smoke_004`: Duration 185.50s, 1 step. Step 1 watchdog timeout; unhandled cancellation dropped telemetry.
  5. `qwen3_smoke_005`: Duration 188.56s, 1 step. Step 1 watchdog timeout; dedicated `except asyncio.CancelledError:` successfully captured in-flight telemetry.
- **Scientific Scoping:** These 5 runs are exploratory systems telemetry diagnosing local hardware limits and watchdog mechanics. They do not constitute a generalizable capability benchmark.

---

## 6. Statistical Engine and Power Simulation Inventory

- **Scripts:** `analyze_v3_results.py`, `power_analysis.py`, `reproduce_power_audit.py`
- **Output Artifacts:** `power_audit_results.json`, `test_scratch_synthetic_data/`
- **Verified Mathematical Properties:**
  1. **Newcombe Hybrid Score CI:** Matches Newcombe (1998) Table II reference data to 4 decimal places ($\hat{\theta} = 0.3250$, 95% CI: $[+0.1764, +0.4578]$).
  2. **Continuity-Corrected CMH Statistic:** Matches Agresti (2002) Table 6.6 clinical data ($\chi^2 = 6.3841, p = 0.0115$).
  3. **Monte Carlo Power:** Under RCBD simulation ($n=20$/arm, $N=80$, 10,000 replications, task log-odds variance $\sigma^2 = 0.09$):
     - Large effect ($\Delta = 0.70$): Power is $98.6\% \pm 0.3\%$.
     - Moderate effect ($\Delta = 0.35$): Power is $49.6\% \pm 1.1\%$.
     - Small effect ($\Delta = 0.20$): Power is $10.8\% \pm 0.6\%$ ($\alpha = 0.0167$).
  4. **TOST Equivalence Sample Size:** Under $\alpha = 0.05, \text{Power} = 0.80, \delta = \pm 0.10$:
     - $p = 0.70 \implies n = 359.8 \approx 360$/arm ($N = 1,440$ for 4 arms).
     - $p = 0.50 \implies n = 428.3 \approx 429$/arm ($N = 1,716$ for 4 arms).
     - Clustered ($\text{DEFF} = 1.30$) $\implies n \approx 468$/arm.

---

## 7. Claim-to-Evidence Classification Matrix

| Claim in Previous Manuscript | Evidence Source | Type of Evidence | Status | Required Revision / Correction |
| :--- | :--- | :--- | :--- | :--- |
| **"Schema.org JSON-LD has 0% reachability to LLM prompts"** | `serializer.py:L18`, `audit_metadata_reachability.py` | Static code AST + Dynamic execution trace | **SUPPORTED** | Scope explicitly to `browser-use 0.13.10` observation serialization path. Note out-of-band JS evaluation can access script text. |
| **"Non-interactive ARIA semantics are 100% stripped"** | `serializer.py:L1046`, `audit_metadata_reachability.py` | Static code AST + Dynamic execution trace | **SUPPORTED** | Retain claim with clear distinction between interactive tags and non-interactive container tags. |
| **"27 of 34 interactive elements match Blink AXTree"** | `compare_accessibility_tree.py`, `accessibility_tree_comparison.json` | Dynamic execution measurement | **SUPPORTED** | Disclose that 34 elements are a complete route census; identify the 7 unmatched elements as `<span class="product-stock in-stock">`. |
| **"AXTree is Stage 3 in a 5-stage serial pipeline"** | Architectural inspection of `browser_use/dom/` | Architectural inspection | **CONTRADICTED** | **Correct architecture:** AXTree is NOT a serial intermediary; it is a parallel browser representation. Serializer walks live DOM directly. |
| **"Cloud pilot proves semantic markup does not improve performance"** | `results/v3_3arm_summary.csv` | Dynamic execution data | **UNSUPPORTED / OVERCLAIM** | **Downgrade:** Control arm achieved 100% completion; result is an empirical ceiling effect on simple tasks, not evidence of markup uselessness or equivalence. |
| **"Qwen trials demonstrate LLM context evaluation scaling laws"** | `results/local_llama_summary.csv` | Exploratory diagnostic ($N=5$) | **PARTIALLY SUPPORTED** | Relocate to engineering telemetry appendix. Clarify that 5 runs on 4 GB VRAM illustrate local hardware timeouts, not generalizable scaling. |
| **"Deterministic API Quota Governance guarantees multi-process budgets"** | `budget_controller.py` | Implementation inspection | **PARTIALLY SUPPORTED** | Clarify scope: single-process Python thread lock (`threading.RLock`); does not provide inter-process distributed locking or billing console caps. |
| **"Synthetic benchmark tables (Tables 3 & 4) represent agent capabilities"** | `test_scratch_synthetic_data/` | Synthetic software tests | **CONTRADICTED** | Synthetic mock data. Relocate from main empirical narrative to software validation appendix with prominent disclaimers. |
| **"Citation to AgentOccam (ICLR 2025)"** | `references.bib` | Bibliographic record | **CONTRADICTED** | Correct hallucinated authors (Yue Yang et al.) to canonical author list: Ke Yang, Yao Liu, Sapana Chaudhary, et al. (arXiv:2410.13825, ICLR 2025). |
| **"Citation to OSWorld (NeurIPS 2024)"** | `references.bib` | Bibliographic record | **CONTRADICTED** | Correct hallucinated author names (Han Shen, etc.) to canonical 17-author list (Tianbao Xie et al., NeurIPS 2024). |

---

## 8. Audit Verdict

The core systems findings (deterministic serializer pruning, non-interactive tag stripping, attribute whitelisting, and structural divergence with Chromium AXTree) are solidly verified in source code and reproducible traces. However, the manuscript requires:
1. Re-centering on the observation pipeline systems audit (single-framework case study).
2. Elimination of the false sequential AXTree pipeline stage in favor of parallel representation paths.
3. Explicit disclosure of the cloud pilot's ceiling effect without overclaiming.
4. Relocation of synthetic benchmark tables, Qwen debugging runs, and quota governance code to appendices.
5. Bibliographic corrections for AgentOccam and OSWorld.
