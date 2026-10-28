# Reproducibility Checklist & Protocol Execution Guide
**Protocol Version:** v3  
**Date:** 2026-10-18  

This checklist provides a step-by-step verification procedure for reproducing the benchmark environment, executing the offline validation suite, and preparing for prospective experimental runs.

---

## 1. Environment & Dependency Audit
- [ ] **Python Interpreter:** Python 3.11.x (confirmed 3.11.9 at `C:\testing\.venv311\Scripts\python.exe`).
- [ ] **Browser Automation Stack:** `browser-use == 0.13.10` and `playwright == 1.48.0`.
- [ ] **Chromium Headless Binary:** Verified installed and executable (`playwright install chromium`).
- [ ] **BeautifulSoup & Parsers:** `beautifulsoup4` and `lxml` available for offline DOM checks.
- [ ] **Deterministic Seed:** Verified that pseudo-random schedule uses fixed seed `seed=42`.

---

## 2. Source File Immutability & Safety Audit
- [ ] **Original Source Files Untouched:**
  - `runner/agent-runner.py` SHA-256 matches baseline.
  - `runner/verifier.py` SHA-256 matches baseline.
  - `tasks/task-definitions.json` SHA-256 matches baseline.
  - `shared/products.js` and `shared/app-core.js` SHA-256 match baseline.
  - All variants in `variants/` (`v0-baseline`, `v1-jsonld`, `v2-aria`, `v3-data-attrs`, `v4-evidence-meta`) match baseline.
- [ ] **Zero Network Access:** All tests executed with zero external socket or HTTP connections.
- [ ] **Zero API Calls:** No LLM provider API invocations during preparation or verification.

---

## 3. Offline Test Suite Execution
- [ ] **Execution Command:**
  ```powershell
  python C:\testing\research_execution_20261018\offline_test_suite.py
  ```
- [ ] **Pass Rate:** 100% of offline tests must pass (0 failures, 0 errors).
- [ ] **Output Artifact:** Verify `offline_test_results.json` generated and populated with actual timestamps and test results.

---

## 4. Prospective Protocol Execution Pre-Flight Checklist
(To be executed ONLY after explicit human protocol approval and API authorization)
- [ ] **Web Server Launch:** Start local static server (`python -m http.server 8080` in `C:\testing`).
- [ ] **Port Verification:** Confirm `http://localhost:8080/variants/v0-baseline/#home` responds with HTTP 200.
- [ ] **API Key Configuration:** Set valid, paid-tier Google API key in environment (`GOOGLE_API_KEY`). Free-tier 500 RPD quota is insufficient for full 96-run experiment.
- [ ] **Vision Confound Guard:** Confirm `use_vision=False` is set in runner initialization.
- [ ] **DATA-CFG Whitelist Patch:** Confirm `EXTENDED_ATTRIBUTES` is passed to agent `include_attributes`.
- [ ] **Pre-Run State Assertion:** Confirm T5 setup script executes and verifies `len(cart) == 1 && cart[0].sku == 'wh-001'` prior to launching agent.
- [ ] **Preregistration Freeze:** Preregister protocol on OSF with hash of `protocol.md` and `task_specifications.json`.
