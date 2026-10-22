# Observation Pipeline Reproducibility Guide: Multi-Stage Reachability Tracing

**Document Version:** 1.0 (Pipeline Reproducibility Specification)  
**Date:** October 22, 2026  
**Auditor / Systems Researcher:** Antigravity Scientific Methodology & Protocol Architecture Team  
**Compliance Status:** 100% Offline · Deterministic Headless Execution  
**Workspace:** [`C:\testing\research_execution_20261018\`](file:///C:/testing/research_execution_20261018/)  

---

## 1. Executive Summary & Purpose

This guide establishes the exact, reproducible methodology for evaluating semantic metadata reachability across the five distinct observation pipeline stages in autonomous browser agents:

$$\text{Source HTML} \longrightarrow \text{Blink AXTree} \longrightarrow \text{browser-use Serializer} \longrightarrow \text{LLM Prompt Buffer} \longrightarrow \text{Auxiliary Channels}$$

It provides step-by-step instructions to reproduce all empirical findings regarding JSON-LD pruning, interactive ARIA delivery, static ARIA pruning, custom `data-*` whitelisting, and Chromium Blink node correspondence.

---

## 2. Environment & Toolchain Dependencies

- **Operating System:** Windows 11 / Windows Server (PowerShell 5.1+ or 7.x).
- **Python Runtime:** Python 3.11.9 (`C:\testing\.venv311\Scripts\python.exe`).
- **Core Libraries:**
  - `browser-use == 0.13.10` ([`browser_use/dom/serializer/serializer.py`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py))
  - `playwright == 0.13.x` / CDP integration
  - Standard library: `http.server`, `asyncio`, `json`, `re`, `unittest`
- **Browser Binary:** Chromium (installed via `browser-use` / Playwright cache).

---

## 3. Step-by-Step Reproduction Procedures

### 3.1 Procedure 1: End-to-End Observation Delivery Verification
Verifies that visible text is delivered across all variants, button ARIA is delivered without target product leakage, static ARIA is pruned, JSON-LD is pruned, and custom `data-*` attributes are exposed only under extended whitelisting.

```bash
# Command:
C:\testing\.venv311\Scripts\python.exe research_execution_20261018/verify_treatment_delivery_e2e.py
```
- **What Runs:** Spawns a background `http.server` on port 8092, navigates a real headless Chromium instance across all 4 variants (`v0-baseline`, `v2-aria`, `v3-data-attrs`, `v1-jsonld`), extracts the serialized DOM via `DOMTreeSerializer`, and asserts attribute presence/absence.
- **Expected Output:**
  ```
  [PASS] v0_visible_text_delivered: True
  [PASS] v0_no_aria_enhancements: True
  [PASS] v0_no_data_actions: True
  [PASS] v2_aria_delivered_on_interactive: True
  [PASS] v2_noninteractive_aria_omitted: True
  [PASS] v3_default_whitelist_strips_data_attrs: True
  [PASS] v3_extended_whitelist_delivers_data_attrs: True
  [PASS] v1_jsonld_pruned_by_serializer: True
  Overall Status: ALL TESTS PASSED
  ```
- **Exit Code:** `0` (Execution time: $\sim 11.0\text{s}$).

---

### 3.2 Procedure 2: Live Agent Observation & Prompt Construction
Verifies that `browser_use.Agent` constructs the final LLM prompt buffer containing exact observed contents without making paid API calls, using a deterministic local `MockChatModel`.

```bash
# Command:
C:\testing\.venv311\Scripts\python.exe research_execution_20261018/test_agent_prompt_pipeline.py
```
- **What Runs:** Spawns local HTTP server on port 8093, instantiates `browser_use.Agent` with `MockChatModel`, executes step 1 navigation across variants, and inspects the raw string contents of `history.model_actions()` and prompt messages.
- **Expected Output:**
  ```
  LIVE AGENT PROMPT PIPELINE TEST RESULTS:
    v0_prompt_has_price_text: True
    v0_prompt_has_soundflow: True
    v0_prompt_has_aria_btn: False
    v0_prompt_has_data_attrs: False
    v2_prompt_has_price_text: True
    v2_prompt_has_aria_btn: True
    v2_prompt_has_aria_price_span: False
    v3_def_prompt_has_data_action: False
    v3_ext_prompt_has_data_action: True
    v3_ext_prompt_has_data_product_id: True
    v3_ext_prompt_has_data_amount: False
    v1_prompt_has_jsonld: False
  ```
- **Exit Code:** `0` (Execution time: $\sim 18.5\text{s}$).

---

### 3.3 Procedure 3: Dynamic CDP AXTree Comparison & Node Correspondence
Measures structural divergence between Chromium Blink's full accessibility tree and `browser-use`'s serialized DOM, pairing interactive elements 1-to-1 via `backendDOMNodeId`.

```bash
# Command:
C:\testing\.venv311\Scripts\python.exe research_execution_20261018/compare_accessibility_tree.py
```
- **What Runs:** Connects to headless Chromium via Chrome DevTools Protocol (CDP), triggers `Accessibility.getFullAXTree`, computes element bounding boxes, runs `DOMTreeSerializer`, and executes `compute_node_correspondence()`.
- **Expected Artifacts Generated:**
  - JSON output: [`research_execution_20261018/accessibility_tree_comparison.json`](file:///C:/testing/research_execution_20261018/accessibility_tree_comparison.json)
  - Markdown report: [`research_execution_20261018/ACCESSIBILITY_TREE_COMPARISON.md`](file:///C:/testing/research_execution_20261018/ACCESSIBILITY_TREE_COMPARISON.md)
- **Key Measured Findings:**
  - Route: `#home`
  - Interactive elements tested: 34
  - Paired 1-to-1 via Blink `backendDOMNodeId`: **27 of 34 ($79.4\%$)**
  - Unmatched elements: 7 (Shadow DOM and non-tabbable inputs)
  - Non-interactive node mapping: Stripped to raw text without node IDs; string-matching is an indirect proxy.

---

## 4. Alternative Channel Exposure Verification

To ensure claims of "unreachability" are appropriately scoped:

1. **Browser JavaScript Evaluation Channel:**
   - Any agent equipped with a JavaScript execution tool (`browser.execute_script()`) can bypass DOM serialization limitations:
     ```javascript
     // JSON-LD retrieval:
     const jsonld = JSON.parse(document.querySelector('script[type="application/ld+json"]').textContent);
     // Dataset attribute retrieval:
     const sku = document.querySelector('.product-card').dataset.sku;
     ```
   - **Conclusion:** JSON-LD and custom `data-*` are **omitted from default serialized prompts**, but **reachable via active code execution**.
2. **Visual Screenshot Channel:**
   - Multimodal agents operating with `use_vision=True` receive raw rendered viewport pixels.
   - Text rendered visually (`$49.99`, `Rating: 4.2`) is directly perceived via OCR/VLM perception, bypassing serializer pruning of `<span aria-label="...">`.
   - Hidden metadata (`data-sku`, JSON-LD) remains completely invisible to vision.
   - **Conclusion:** `use_vision=False` is strictly necessary to evaluate the causal impact of token-based semantic markup.
