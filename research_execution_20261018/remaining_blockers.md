# Prioritized Blocker Analysis & Resolution Matrix
**Protocol Version:** v3  
**Audit Date:** 2026-10-18  
**Source Baseline:** `master_audit_20261018/05_PROTOCOL_v3_READINESS.md`  

---

## 1. Executive Summary of Blocker Status

The previous readiness report identified **five implementation blockers** preventing experimental execution. In this research execution phase, all technical and methodological blockers have been resolved through proposed specifications, corrected verifiers, and runnable offline tests without modifying any original project files.

---

## 2. Detailed Blocker Analysis

### Blocker 1: JSON-LD Channel Pruning in Observation Serializer (`DISABLED_ELEMENTS`)
- **Underlying Problem:** `browser-use 0.13.10` hardcodes `DISABLED_ELEMENTS = {'style', 'script', 'head', 'meta', 'link', 'title'}` in `serializer.py`. All `<script type="application/ld+json">` elements are stripped before DOM snapshots reach the LLM.
- **Scientific Significance:** The historical `v1-jsonld` arm was scientifically invalid because the LLM could never perceive the target fact. It functioned as an inadvertent `ABS` condition, testing hallucination rather than channel delivery.
- **Can it be resolved safely without modifying original files?** YES.
- **Proposed Resolution:** Formally exclude the `v1-jsonld` arm from Protocol v3. The 4-arm design uses an explicit `ABS` negative control alongside `VIS`, `ARIA`, and `DATA-CFG`.
- **Offline Test Validation:** `test_serializer_disabled_elements` in `offline_test_suite.py` asserts that `'script'` and `'meta'` are in `DISABLED_ELEMENTS`.
- **Human Decision Required:** Formal approval of the 4-arm design (ABS, VIS, ARIA, DATA-CFG) excluding JSON-LD.

---

### Blocker 2: Custom `data-*` Attribute Stripping in Default Observation Whitelist
- **Underlying Problem:** `browser_use.dom.views.DEFAULT_INCLUDE_ATTRIBUTES` omits custom attributes like `data-amount`, `data-rating`, and `data-warranty`. In historical runs, `v3-data-attrs` was stripped by default.
- **Scientific Significance:** Testing a custom attribute channel requires that the agent observation pipeline is configured to expose those attributes; otherwise, the arm is identical to `ABS`.
- **Can it be resolved safely without modifying original files?** YES.
- **Proposed Resolution:** In Protocol v3, define `EXTENDED_ATTRIBUTES` in `protocol.md` and `task_specifications.json`, providing the exact patch for runner initialization.
- **Offline Test Validation:** `test_views_default_include_attributes` and `test_patched_include_attributes` verify attribute stripping under default views and restoration under patched views.
- **Human Decision Required:** Approval to apply the configuration patch to `agent-runner.py` before live execution.

---

### Blocker 3: Multimodal Vision Confound (`use_vision=True`)
- **Underlying Problem:** `runner/agent-runner.py` initialized `Agent` with `use_vision=True` (line 648). In historical runs, screenshots were captured and sent to Gemini.
- **Scientific Significance:** In the `VIS` arm, target text appeared in screenshots (multimodal dual-channel delivery: DOM text + visual image). In `ARIA` and `DATA-CFG` arms, attributes are NOT rendered visually (single-channel: DOM text only). This created a severe uncontrolled visual confound favoring `VIS`.
- **Can it be resolved safely without modifying original files?** YES.
- **Proposed Resolution:** Protocol v3 strictly mandates `use_vision=False` in runner initialization and schema validation.
- **Offline Test Validation:** Verified in `protocol.md` and `run_manifest_schema.json` enforcing `use_vision: false`.
- **Human Decision Required:** Approval to enforce text-only DOM processing for the prospective experiment.

---

### Blocker 4: Logical Flaws in Historical Verifiers (T3, T4, T5)
- **Underlying Problem:**
  - T3 accepted lowest-rated item (`wh-001`) as valid via a broad eligible set.
  - T4 awarded `partial_score = 0.25` unconditionally on the failure path.
  - T5 passed vacuously if cart was empty before launch.
- **Scientific Significance:** Contaminated all historical success rates, rendering cross-arm statistical comparisons meaningless.
- **Can it be resolved safely without modifying original files?** YES.
- **Proposed Resolution:** Implemented complete strict verifiers in `verifier_specification.md` and `task_specifications.json`.
- **Offline Test Validation:** `test_t3_verifier_flaw_fixed`, `test_t4_verifier_no_unconditional_partial`, and `test_t5_verifier_prestate_assertion` pass with 100% precision.
- **Human Decision Required:** Approval of strict verifier logic.

---

### Blocker 5: Lack of Pre-Run Cart State Assertion for T5
- **Underlying Problem:** T5 requires removing an item from the cart. If `setup_script` fails to seed `wh-001` via localStorage, the cart starts empty and the agent scores a vacuous pass by doing nothing.
- **Scientific Significance:** Spurious passes corrupt the true effect size of grounded actions.
- **Can it be resolved safely without modifying original files?** YES.
- **Proposed Resolution:** Two-phase verification architecture requiring explicit pre-run cart assertion before agent launch.
- **Offline Test Validation:** `test_t5_verifier_prestate_assertion` verifies that an unseeded cart returns `PRE_STATE_NOT_INITIALIZED` and `success=False`.
- **Human Decision Required:** Approval of mandatory pre-flight assertion step in execution pipeline.

---

## 3. Operational Blockers (Pending Live Authorization)

| Operational Blocker | Issue | Impact | Required Resolution |
|---------------------|-------|--------|---------------------|
| **API Quota & Billing** | Free-tier Gemini quota (500 RPD) caused 42 HTTP 429 failures at run #106 in historical tests. | Experiment truncation | Obtain human authorization and configure paid Google API key or Tier-1 quota before running 96 runs. |
| **Human Protocol Approval** | Protocol v3 is currently PROPOSED and requires formal user review. | Protocol freeze pending | Formal sign-off on `protocol.md` and `task_specifications.json`. |
