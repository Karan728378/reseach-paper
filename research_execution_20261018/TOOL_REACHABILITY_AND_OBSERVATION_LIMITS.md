# TOOL REACHABILITY AND OBSERVATION LIMITS AUDIT

**Target:** Disentangling Observation Omission from Functional Inaccessibility  
**Host Workspace:** `C:\testing\research_execution_20261018`  
**Audit Date:** 2026-10-25  

---

## 1. The Critical Theoretical Distinction

A core vulnerability in autonomous agent literature is conflating **observation omission** with **systemic inaccessibility**:
- **Observation Omission:** An attribute or element is absent from the initial text serialized into the agent's observation prompt (e.g., pruned by `DISABLED_ELEMENTS` or discarded container attributes).
- **True Inaccessibility:** An attribute or element cannot be retrieved, inspected, or acted upon by the agent through any available tool, API, or modality.

In modern agent architectures equipped with dynamic tool execution (e.g., `evaluate_script`, `extract_content`, `take_screenshot`), an omission from the initial DOM observation does **not** preclude the agent from discovering the target fact if it possesses the procedural knowledge to invoke retrieval tools.

---

## 2. Multi-Channel Reachability Matrix

The following matrix documents reachability across observation and tool retrieval pathways:

| Information Channel | Initial Observation (Serialized Prompt) | Internal DOM Snapshot | Direct Tool Retrieval Available? | Specific Recovery Mechanism | Model Context Verified? | Evidence Status |
| :--- | :---: | :---: | :---: | :--- | :---: | :--- |
| **Visible Body Text** | Preserved | Preserved | Yes | Default text observation buffer | Yes | REPRODUCED OFFLINE |
| **Interactive Form Controls** | Preserved with `[index]` | Preserved | Yes | `click_element(index)`, `input_text(index)` | Yes | REPRODUCED OFFLINE |
| **Hidden `<script>` (JSON-LD)** | **Omitted** | Omitted | **Yes** | `evaluate_script("JSON.parse(document.querySelector('script[type=\"application/ld+json\"]').textContent)")` | No (requires explicit tool action) | REPRODUCED OFFLINE |
| **Header `<meta>` Tags** | **Omitted** | Omitted | **Yes** | `evaluate_script("document.querySelector('meta[name=\"...\"]').content")` | No (requires explicit tool action) | REPRODUCED OFFLINE |
| **Page `<title>`** | **Omitted** | Omitted | **Yes** | `evaluate_script("document.title")` or session URL/title telemetry | Yes (in browser title bar) | REPRODUCED OFFLINE |
| **Dataset (`data-*`) on Non-Interactive Tags** | **Omitted** | Preserved in snapshot | **Yes** | `evaluate_script("document.querySelector('span.sku').dataset.sku")` | No (requires explicit tool action) | REPRODUCED OFFLINE |
| **ARIA Labels on Non-Interactive Tags** | **Omitted** | Preserved in snapshot | **Yes** | `evaluate_script("document.querySelector('span').getAttribute('aria-label')")` | No (requires explicit tool action) | REPRODUCED OFFLINE |
| **Shadow DOM Encapsulated Nodes** | **Partial** | Partial | **Yes** | Playwright pierce selectors (`page.locator('css=>>>button')`) | Partial | SUPPORTED BUT LIMITED |
| **Visual / Spatial Layout Layouts** | **Omitted in Text** | Preserved | **Yes** | Multimodal Vision (`take_screenshot`, bounding box inspection) | Yes (when `use_vision=True`) | REPRODUCED OFFLINE |
| **Absent / Non-Existent Fact** | **Absent** | Absent | **No** | None (requires appropriate refusal / abstain response) | N/A | VERIFIED FROM PRIMARY EVIDENCE |

---

## 3. Empirical Proof via Sentinel Fixture Tests

To verify that omitted attributes remain recoverable via direct tools without executing live LLM calls, we evaluated `test_sentinel_pipeline.py` against `fixtures/sentinel_fixture.html`:
1. **JSON-LD Recovery:** While `<script type="application/ld+json">` is pruned from the serialized prompt by `DISABLED_ELEMENTS`, Playwright evaluation `evaluate_script("document.querySelector('script[type=\"application/ld+json\"]').textContent")` returns the JSON payload with 100% fidelity.
2. **Container `data-*` Recovery:** `<span class="product-sku" data-sku="WH-1000XM4">` loses `data-sku` in the text serializer, but `evaluate_script("document.querySelector('.product-sku').getAttribute('data-sku')")` retrieves `"WH-1000XM4"` deterministically.
3. **Synthetic Fixture Labeling:** These mechanism tests are conducted on controlled synthetic fixtures to validate software pipeline mechanics; they do **not** represent real-world agent task success distributions.
