# PHASE 1 BASELINE AUDIT: REPOSITORY FORENSICS & VERIFICATION

**Project Title:** The DOM Serialization Gap: Evaluating Additive Semantic Markup and Observation-Pipeline Bottlenecks in Autonomous Browser Agents  
**Workspace:** [`C:\testing\research_execution_20261018\`](file:///C:/testing/research_execution_20261018/)  
**Python Runtime Inspected:** [`C:\testing\.venv311\Scripts\python.exe`](file:///C:/testing/.venv311/Scripts/python.exe) (`browser-use 0.13.10`)  
**Audit Date:** October 21, 2026  
**Auditor:** Research Supervisor & Lead Technical Auditor  

---

## 1. Overview & Forensic Verification Methodology

This document establishes the verified, indisputable baseline of the research codebase. Every statement in this audit has been directly confirmed through:
1. Static code inspection of the installed library files in [`C:\testing\.venv311\Lib\site-packages\browser_use\`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/).
2. Execution of the local test suites: [`offline_test_suite.py`](file:///C:/testing/research_execution_20261018/offline_test_suite.py) (11 tests), [`test_analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/test_analyze_v3_results.py) (11 tests), and [`test_agent_prompt_pipeline.py`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py) (5 prompt inspection scenarios).
3. Inspection of data provenance inventories: [`DATASET_INVENTORY.csv`](file:///C:/testing/research_execution_20261018/DATASET_INVENTORY.csv), [`DATA_PROVENANCE_AUDIT.md`](file:///C:/testing/research_execution_20261018/DATA_PROVENANCE_AUDIT.md), and [`EMPIRICAL_RESULTS_STATUS.md`](file:///C:/testing/research_execution_20261018/EMPIRICAL_RESULTS_STATUS.md).

No assumptions from prior conversational turns have been taken for granted; all findings have been re-verified against ground-truth source code.

---

## 2. Verified Architectural Findings (`browser-use 0.13.10`)

### 2.1 Fatal JSON-LD Pruning (`DISABLED_ELEMENTS`)
- **Source Location:** [`C:\testing\.venv311\Lib\site-packages\browser_use\dom\serializer\serializer.py:Line 18`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L18)
  ```python
  DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}
  ```
- **Pruning Implementation:** [`serializer.py:Lines 480–482`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L480-L482)
  ```python
  elif node.node_type == NodeType.ELEMENT_NODE:
      # Skip non-content elements
      if node.node_name.lower() in DISABLED_ELEMENTS:
          return None
  ```
- **Verified Outcome:** Any `<script type="application/ld+json">` node is pruned during DOM simplification. Child text is never traversed. Live execution of [`test_agent_prompt_pipeline.py`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py) confirms that 0 tokens of Schema.org JSON-LD data reach the model message buffer (`v1_prompt_has_jsonld: False`).

### 2.2 The Non-Interactive Attribute Drop (Critical Architectural Discovery)
- **Source Location:** [`serializer.py:Lines 1046–1058`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L1046-L1058)
  ```python
  # Add element if clickable, scrollable, or iframe
  is_any_scrollable = node.original_node.is_actually_scrollable or node.original_node.is_scrollable
  should_show_scroll = node.original_node.should_show_scroll_info
  if (
      node.is_interactive
      or is_any_scrollable
      or node.original_node.tag_name.upper() == 'IFRAME'
      or node.original_node.tag_name.upper() == 'FRAME'
  ):
      ...
      attributes_html_str = DOMTreeSerializer._build_attributes_string(
          node.original_node, include_attributes, text_content
      )
  ```
- **Verified Outcome:** In `browser-use`, element strings and attribute sets are constructed **only for interactive elements, scrollable containers, or iframes**. Non-interactive informational elements (`<span class="product-price">`, `<div class="rating">`, `<p class="warranty">`) have their tags stripped entirely.
- **Dynamic Confirmation:** In `v2-aria`, `<span aria-label="Price: $49.99">` has its `aria-label` dropped (`v2_prompt_has_aria_price_span: False`). In `v3-data-attrs`, `<span data-amount="49.99">` has its `data-amount` dropped (`v3_ext_prompt_has_data_amount: False`). Only interactive `<button>` tags retain attributes.

### 2.3 Attribute Whitelist Filtering
- **Source Location:** [`C:\testing\.venv311\Lib\site-packages\browser_use\dom\views.py:Line 18`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/views.py#L18) and [`serializer.py:Lines 1211–1215`](file:///C:/testing/.venv311/Lib/site-packages/browser_use/dom/serializer/serializer.py#L1211-L1215)
- **Verified Outcome:** `DEFAULT_INCLUDE_ATTRIBUTES` omits custom developer attributes (`data-action`, `data-product-id`, `data-amount`). In default configurations, custom attributes are stripped even from buttons (`v3_def_prompt_has_data_action: False`). They survive on buttons if and only if `EXTENDED_ATTRIBUTES` is explicitly injected via `Agent(include_attributes=...)` ([`protocol_v3_runner.py:L32`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L32)).

---

## 3. Inventory of Existing Tests and What They Actually Prove

| Test Suite | File Location | Tests | Execution Status | What It Actually Proves | What It Does NOT Prove |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **Statistical Pipeline Unit Tests** | [`test_analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/test_analyze_v3_results.py) | 11 | **PASS** (0.22s) | Mathematical correctness of CMH, Newcombe CIs, Fisher test, Bonferroni adjustments against published literature (Agresti 2002, Newcombe 1998). | Does not prove agent performance. Only proves calculation correctness over CSV inputs. |
| **Offline Verification Suite** | [`offline_test_suite.py`](file:///C:/testing/research_execution_20261018/offline_test_suite.py) | 11 | **PASS** (0.15s) | Confirms static source properties: `DISABLED_ELEMENTS`, whitelist behavior, verifier logic fixes (T3/T4/T5), RCBD schedule balance. | Does not evaluate LLM reasoning or prompt reachability dynamically. |
| **Live Prompt Pipeline Verification** | [`test_agent_prompt_pipeline.py`](file:///C:/testing/research_execution_20261018/test_agent_prompt_pipeline.py) | 5 scenarios | **PASS** (25.1s) | Dynamically verifies that `browser-use` extracts text into prompt buffer, retains button attributes, strips JSON-LD, and strips non-interactive attributes. | Uses `FakeListChatModel`; does not measure whether an actual frontier LLM behaves differently on the prompt. |

---

## 4. Verification of Live-Experiment Status & Provenance Accounting

| Dataset Identifier | File Path | Record Count | Modality | Integrity Status | Confirmatory Eligibility |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **Historical Pilot (Exp 1)** | [`results/pilot-summary-clean.csv`](file:///C:/testing/results/pilot-summary-clean.csv) | 250 rows | `use_vision=True` | **Compromised:** Pruned treatments (JSON-LD stripped), loose verifiers (T3 passed 6 SKUs), repetition 9 survivorship bias. | **Ineligible (Excluded).** Historical artifact only. |
| **Aborted Main Run (Exp 1b)** | [`results/main_experiment/full-summary.csv`](file:///C:/testing/results/main_experiment/full-summary.csv) | 147 rows | `use_vision=True` | **Truncated:** Free-tier quota crashed at run 105; 42 consecutive HTTP 429 aborts. | **Ineligible (Discontinued).** |
| **Synthetic Benchmark** | [`test_scratch_synthetic_data/dataset_1_valid_complete.csv`](file:///C:/testing/research_execution_20261018/test_scratch_synthetic_data/dataset_1_valid_complete.csv) | 96 rows | N/A (Mock) | **Software Validation Benchmark:** Deterministic test fixture. | **Ineligible (Mock Data).** Must not be reported as empirical results. |
| **Protocol v3 Confirmatory Trials** | [`proposed_randomized_schedule.csv`](file:///C:/testing/research_execution_20261018/proposed_randomized_schedule.csv) | 96 scheduled | `use_vision=False` | **Unexecuted:** [`protocol_v3_runner.py:L258`](file:///C:/testing/research_execution_20261018/protocol_v3_runner.py#L258) has `SAFETY_GATE_LOCKED = True`. | **0 of 96 Completed.** |

---

## 5. Audit of Discrepancies, Flaws & Unverified Claims

### 5.1 Discrepancy 1: Manuscript Results Table vs. Empirical Reality
- **Issue:** [`RESEARCH_PAPER_DRAFT.md:Lines 316–333`](file:///C:/testing/research_execution_20261018/RESEARCH_PAPER_DRAFT.md#L316-L333) displays full statistical contrast tables (Risk Difference $= +0.0750$, CMH $p = 0.7662$, etc.).
- **Reality:** These figures derive entirely from `dataset_1_valid_complete.csv` (synthetic mock data). While disclaimers exist in the draft, presenting mock numbers in Section 10 results tables creates an unacceptable risk of misinterpretation.

### 5.2 Discrepancy 2: Claiming "Additive Semantic Markup" When Only Buttons Differ
- **Issue:** The study claims to evaluate the additive effect of WAI-ARIA and `data-*` attributes across an e-commerce website.
- **Reality:** Because `browser-use` strips attributes on non-interactive elements, the only attribute surviving to the LLM prompt in `v2-aria` is on `<button>` elements (`aria-label="Add SoundFlow Air 3 to cart"`). This confounds semantic accessibility with button text disambiguation and target-text co-location.

### 5.3 Discrepancy 3: Sample Size Underpowering vs. Web Standards Claims
- **Issue:** Early drafts suggested that finding $p > 0.05$ would provide evidence that web developers do not need to augment websites with ARIA for AI agents.
- **Reality:** With $n=20$ per arm on primary tasks T1–T5, power to detect small effect sizes ($\Delta \le 0.20$) is $<11\%$ ([`power_analysis.json:L85`](file:///C:/testing/research_execution_20261018/power_analysis.json#L85)). An underpowered non-significant result cannot support equivalence claims without committing the Equivalence Fallacy.

---

## 6. Baseline Scorecard (Starting Point Before Redesign)

| # | Major Dimension | Baseline Score | Primary Justification |
| :-: | :--- | :-: | :--- |
| **1** | **Research Question** | **4.5 / 10** | Broad question collapsed into narrow button-label ablation. |
| **2** | **Novelty** | **5.0 / 10** | Serializer pruning is novel; toy store ablation has minimal novelty. |
| **3** | **Practical Contribution** | **5.5 / 10** | Warning on serializer pruning is useful; toy store results lack external validity. |
| **4** | **Code Quality** | **8.5 / 10** | High-quality tests, robust runners, clean separation. |
| **5** | **DOM Serialization Verification** | **9.0 / 10** | Excellent static and dynamic prompt verification. |
| **6** | **Experiment Design** | **3.5 / 10** | Confounded button labels; baseline pooling vulnerable to low power. |
| **7** | **Task Realism** | **3.0 / 10** | Single 6-item synthetic store; single model. |
| **8** | **Verifiers** | **8.0 / 10** | Hardened, state-asserted verifiers eliminate earlier scoring flaws. |
| **9** | **Statistics & Power** | **4.0 / 10** | Math is flawless, but $n=20$/arm has $<11\%$ power. |
| **10** | **Data Provenance** | **8.5 / 10** | Rigorous forensic audit and quarantine of compromised historical data. |
| **11** | **Literature Review** | **7.5 / 10** | Authentic citations; claims of "first study" require qualification. |
| **12** | **Manuscript Quality** | **4.0 / 10** | Reports synthetic data in main results tables. |
| **13** | **Feasibility** | **8.5 / 10** | Offline suite runs locally in seconds for $0.00. |
| **14** | **Publication Potential** | **3.5 / 10** | 0% at major conferences; viable only as a student workshop systems paper. |
| **15** | **Project Maturity** | **6.0 / 10** | Code is complete; empirical live data is at 0%. |

---

## 7. Phase 1 Conclusion & Transition Gate

The baseline audit confirms that the project's software engineering and systems discovery are sound, but its empirical behavioral experiment cannot stand in its current form. 

**Transition Gate Approved:** Proceed to **Phase 2 (Research Question, Scope, and Novelty Redesign)** to formally reframe the study around Direction B.
