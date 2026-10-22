# 09. Zero-API Offline Implementation & Verification Test Results

**Audit Directory:** `C:\testing\research_audit_20261015_231500`  
**Date:** 2026-10-17  
**Auditor:** Antigravity Senior Empirical Research & Reproducibility Team  

---

## 1. Summary of Executed Offline Tests

All tests were executed entirely offline using the local Python environments (`.venv` and `.venv311`) with **ZERO calls to LLM APIs, ZERO network requests, and ZERO quota consumption**.

### Table 1: Comprehensive Offline Test Suite Results

| Test Category | Test Script / Fixture | Tested Component | Expected Outcome | Observed Outcome | Status |
|---|---|---|---|---|---|
| **File Integrity** | `make_manifest.py` | Full project tree (2012 files) | SHA-256 hashes generated; zero file modification | 2012 files hashed into `01_FILE_HASH_MANIFEST.csv` | **PASS** |
| **Verifier Accuracy** | `test_offline_suite.py` | T1 SKU matching (`wh-001`) | Exact match succeeds; wrong SKU and empty cart fail | Exact SKU equality verified; substring collisions rejected | **PASS** |
| **Verifier Accuracy** | `test_offline_suite.py` | T2 SKU matching (`mkp-001`) | Exact match succeeds; wrong SKU fails | Exact SKU equality verified | **PASS** |
| **Verifier Flaw Detection** | `test_offline_suite.py` | T3 second-highest rating check | Should only accept `wh-002` (4.5 stars) | Accepts `wh-001` (4.2), `wh-003` (4.8), and `mkp-001` (keyboard) | **FLAW CONFIRMED** |
| **Verifier Bug Detection** | `test_offline_suite.py` | T4 order verifier partial score | Score 0.0 when order not placed | Unconditionally awards 0.25 points even when `order_confirmed=False` | **BUG CONFIRMED** |
| **Verifier Flaw Detection** | `test_offline_suite.py` | T5 empty cart check | Detects whether item was added and removed | Unseeded empty cart scores 1.0 (Success) with 0 agent action | **FLAW CONFIRMED** |
| **Variant Content Parity** | `test_offline_suite.py` | `variants/v0-v4` vs `shared/products.js` | All variants share identical underlying catalog facts | Verified: all variants load identical product objects from `shared/products.js` | **PASS** |
| **Observation Exposure** | `run_channel_exposure_matrix_fixed.py` | Default browser-use pipeline | Tests default token reach | Visible text & interactive ARIA reach prompt; `data-*`, JSON-LD, meta stripped | **VERIFIED** |
| **Observation Exposure** | `run_channel_exposure_matrix_fixed.py` | Configured attribute whitelist | Tests `include_attributes` reach | Interactive `data-*` reaches prompt; non-interactive elements stripped | **VERIFIED** |
| **Observation Exposure** | `run_channel_exposure_matrix_fixed.py` | Patched serializer pipeline | Tests monkey-patched serializer | Non-interactive `data-*` and `<time datetime>` reach prompt | **VERIFIED** |
| **Observation Exposure** | `run_channel_exposure_matrix_fixed.py` | Full observable pipeline | Tests custom python metadata hook | JSON-LD reaches model as message header; 0% exposure in DOM tree | **VERIFIED** |
| **Power Calculation** | `calculate_power.py` | Statistical power across effect sizes | Recomputes sample size from scratch | Power curves verified across $\Delta \in [0.15, 0.70]$ | **PASS** |

---

## 2. Detailed Findings on Verifier Flaws

### 1. T3 Permissive Ground Truth Set
In [`runner/verifier.py:61-64`](file:///C:/testing/runner/verifier.py#L61-L64), `GROUND_TRUTH["T3"]["eligible_skus"]` was defined as `{"wh-001", "wh-002", "wh-003", "mkp-001", "mon-001", "acc-001"}`.
- Running `test_t3_flaw_detection()` proved that an agent adding the *lowest-rated* product (`wh-001`, 4.2 stars) or a *keyboard* (`mkp-001`) receives a perfect score of `1.0`.
- In Protocol v3, this is corrected: `eligible_skus` must contain strictly `{"wh-002"}`.

### 2. T4 Unconditional Partial Scoring
In [`runner/verifier.py:479`](file:///C:/testing/runner/verifier.py#L479), `score += 0.25 # checkout reached` is added without checking whether the checkout URL was reached.
- Running `test_t4_order_verifier_cases()` confirmed that runs where checkout was never initiated receive a partial score of `0.25`.
- In Protocol v3, this line is removed: partial credit is strictly conditional on verified URL navigation.

### 3. T5 Cart Seeding Vulnerability
In [`runner/verifier.py:458-463`](file:///C:/testing/runner/verifier.py#L458-L463), `verify_cart_state([], "T5")` returns `{"success": True, "partial_score": 1.0}`.
- Running `test_t5_unseeded_cart_flaw()` confirmed that if cart pre-seeding fails or is omitted, an idle agent receives a 100% success score.
- In Protocol v3, T5 is replaced with a clean fact-retrieval task to avoid browser-state pre-injection dependencies.
