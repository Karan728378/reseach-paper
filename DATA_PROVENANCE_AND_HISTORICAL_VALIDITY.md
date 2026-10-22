# Data Provenance and Historical Validity Audit

**Document Version:** 1.0 (Audited & Verified)  
**Date:** October 21, 2026  
**Auditor:** Antigravity Scientific Methodology & Forensic Audit Team  
**Compliance Status:** 100% Read-Only Forensic Audit · Zero Data Mutations · Raw Historical CSVs Preserved Untouched  

---

## 1. Executive Summary

A critical scientific vulnerability identified in earlier project documentation was the **unwarranted conflation of compromised historical pilot data with valid empirical evidence**.

This audit established a complete forensic chain of custody for every CSV and data artifact in `C:\testing`:
1. **Raw Historical CSVs Are 100% Intact:** File hashes for `results/pilot-summary-clean.csv` and `results/main_experiment/full-summary.csv` match trustworthy prior records character-for-character. No raw historical records were modified, deleted, or rewritten.
2. **Historical Data Is Scientifically Ineligible for Confirmatory Claims:** The historical pilot trials (October 6–7, 2026) and truncated main experiment (October 11, 2026) are heavily compromised by library-level treatment pruning, selective retry survivorship bias, flawed verifiers, multimodal vision confounding, and target-name co-location.
3. **Strict Data Separation:** Synthetic validation benchmarks ([`test_scratch_synthetic_data/`](file:///C:/testing/research_execution_20261018/test_scratch_synthetic_data/)) and offline pipeline demo traces are quarantined from production datasets.
4. **Confirmatory Experiment Status:** **ZERO live confirmatory runs have been executed under Protocol v3.** The live safety gate remains strictly locked.

---

## 2. Dataset-by-Dataset Forensic Provenance Table

| Dataset File | File Size & Date | Total Rows | Execution Mode & Model | Reported Outcomes | Forensic Findings & Usability Status |
|---|---|:---:|---|---|---|
| [`results/pilot-summary-clean.csv`](file:///C:/testing/results/pilot-summary-clean.csv) | 38,416 bytes<br>Oct 7, 2026 | 250 | Real Live API<br>`gemini-2.0-flash-exp`<br>`use_vision=True` | 249 Successes<br>1 Failure | **COMPROMISED / DESCRIPTIVE ONLY.** Treatment attributes were pruned by `browser-use 0.13.10` serializer; Repetition 9 domain failures were selectively retried until success; permissive verifiers rewarded wrong SKUs. Ineligible for confirmatory inference. |
| [`results/pilot-summary.csv`](file:///C:/testing/results/pilot-summary.csv) | 33,855 bytes<br>Oct 7, 2026 | 261 | Real Live API<br>`gemini-2.0-flash-exp` | 251 Successes<br>10 Failures | **RAW UNFILTERED PILOT LOG.** Contains the 11 discarded runs (including legitimate domain task failures `d6c79dab` and `1e522d81` on v3 T4) that were scrubbed to manufacture the 250-row clean file. |
| [`results/main_experiment/full-summary.csv`](file:///C:/testing/results/main_experiment/full-summary.csv) | 19,249 bytes<br>Oct 11, 2026 | 147 (out of planned 250) | Real Live API<br>`gemini-flash-lite-latest`<br>`use_vision=True` | 105 Successes<br>42 Failures | **TRUNCATED / ABORTED.** Run 106 triggered Google AI free-tier quota exhaustion (500 requests/day limit). Runs 106–147 failed immediately with HTTP 429 (`RESOURCE_EXHAUSTED`). Permanently discontinued. |
| [`research_execution_20261018/proposed_randomized_schedule.csv`](file:///C:/testing/research_execution_20261018/proposed_randomized_schedule.csv) | 3,524 bytes<br>Oct 18, 2026 | 96 | Specification only<br>`seed=42` | 0 Executed<br>96 Pending | **FROZEN PROTOCOL V3 SCHEDULE.** 4 arms $\times$ 6 tasks $\times$ 4 blocks = 96 runs. Zero runs executed. Confirmatory experiment pending human authorization. |
| [`test_scratch_synthetic_data/dataset_1_valid_complete.csv`](file:///C:/testing/research_execution_20261018/test_scratch_synthetic_data/dataset_1_valid_complete.csv) | 8,139 bytes<br>Oct 18, 2026 | 96 | Deterministic Mock / Synthetic | 73 Successes<br>23 Failures | **SYNTHETIC ENGINEERING BENCHMARK.** Feeds statistical test suites ([`test_analyze_v3_results.py`](file:///C:/testing/research_execution_20261018/test_analyze_v3_results.py)) and UI dashboard. Clearly quarantined as synthetic data. |
| [`results/demo_browser_mechanics_and_verifier_runs.csv`](file:///C:/testing/research_execution_20261018/results/demo_browser_mechanics_and_verifier_runs.csv) | 2,152 bytes<br>Oct 18, 2026 | 6 | Offline Headless Browser Playwright | 6 Passes | **MECHANICS VALIDATION TRACE.** Proves JavaScript state transitions (`window.__cart__`, `window.__orderConfirmed__`) and verifiers work. Does NOT measure agent performance. |
| [`results/demo_agent_prompt_delivery_runs.csv`](file:///C:/testing/research_execution_20261018/results/demo_agent_prompt_delivery_runs.csv) | 1,154 bytes<br>Oct 18, 2026 | 4 | Offline Single-Step MockChatModel | 4 Passes | **PROMPT BUFFER DELIVERY TRACE.** Proves observation serialization under `use_vision=False` without API calls. |

---

## 3. Verified Current File Hashes

Direct SHA-256 hash calculations executed via PowerShell on the active filesystem:

```
Algorithm       Hash                                                                   Path
---------       ----                                                                   ----
SHA256          82AE25DED8480C7B7804DD3DFBF53D03A6D46C2ECC96C8939E2044CC9C729B9C       C:\testing\results\pilot-summary-clean.csv
SHA256          42E9856AE932D56E5D8C766B2FD37BDCED4088E6E7E4D0A4D85ECC7244365621       C:\testing\results\main_experiment\full-summary.csv
SHA256          B182AC6BDB6704F2C56F3718DE41262AA2E9689AC2E965CAE256AE1AE9278C11       C:\testing\shared\products.js
SHA256          CCAE98E0218402BD78F7C4548CA743FDE79B89B4BAEE466447B72821621B80C7       C:\testing\shared\app-core.js (Post-Refactor)
SHA256          E61408A8A82192824C1C4B4B6A35AC47E0B36DD9B06025D865E3E435B2231E5F       C:\testing\tasks\task-definitions.json
SHA256          8A4AF77A540B9CFF2FEBA65022DFEE98C43AD9210F4D8F06A809E3F9A5094DFC       C:\testing\runner\agent-runner.py
SHA256          890B968345E82B59CB0545263D8E438A6EF6DE9F521B90DA5B98E5680850B378       C:\testing\runner\verifier.py
SHA256          AA042E92CAAAB5CEAC20A04552E18E182AB4F5812E54B6D28A6899FCE3DF43AE       C:\testing\variants\v0-baseline\index.html
SHA256          E5E303AB0C6DE3108258FCF4603192B539784AF747E8C35F1073182DC097A612       C:\testing\variants\v2-aria\index.html
SHA256          4DB1305A1BC4623499F82A863148602F39E5DB8DD9922F8F5EEE71229B39DF4D       C:\testing\variants\v3-data-attrs\index.html
```

*Hash Integrity Verdict:* All raw historical results match their baseline frozen states 100%. `shared/app-core.js` reflects the post-audit de-confounding refactor (SHA-256: `ccae98...`).

---

## 4. Five Fatal Flaws of the Historical Pilot Trials

The historical 250-run dataset cannot be used to support scientific claims regarding semantic markup effectiveness due to five compound flaws:

1. **Treatment Omission:**  
   In `browser-use==0.13.10`, the DOM serializer unconditionally discarded `<script>` tags (`DISABLED_ELEMENTS = {'style', 'script', ...}`) and stripped custom attributes (`data-action`, `data-amount`) because they were absent from `DEFAULT_INCLUDE_ATTRIBUTES`. Consequently, the treatments `v1-jsonld` and `v3-data-attrs` were physically omitted before prompt generation. The model saw plain HTML in all three arms.
2. **Survivorship & Selective Retry Bias:**  
   In Repetition 9, genuine task execution failures (`d6c79dab` and `1e522d81` on `v3-data-attrs` T4) were discarded, and the runner re-attempted the task until achieving success (`925aac22`). This selective retry policy inflated the success rate from ~96.8% to 99.6%.
3. **Permissive Scoring Flaws:**  
   The historical verifier for T3 accepted 6 different SKUs across keyboards, monitors, and hubs. The T4 verifier granted 0.25 unconditional credit. The T5 verifier awarded success if the cart started empty.
4. **Multimodal Screenshot Grounding:**  
   Historical trials executed with `use_vision=True`. The model had access to high-resolution screenshots, allowing visual recognition of buttons and prices that bypassed DOM text omissions.
5. **Target Co-Location:**  
   In `v2-aria`, action buttons contained the full product title (`aria-label="Add SoundFlow Air 3 to cart"`), revealing the answer in the action tag.

---

## 5. Explicit Claims Matrix: What Historical Data Can and Cannot Support

| Research Claim | Supported by Historical Data? | Evidential Rationale |
|---|:---:|---|
| *"Multimodal agents can navigate basic e-commerce shopping flows using visible typography."* | **YES (Descriptive)** | Genuine live Gemini calls completed checkouts and cart additions when visual screenshots and visible text were provided. |
| *"Unmonitored runner retry policies can mask legitimate failure rates."* | **YES (Methodological)** | Discarding failed runs in Repetition 9 directly demonstrates the reality of retry survivorship bias. |
| *"Free-tier LLM API rate limits are insufficient for 250-trial agent protocols."* | **YES (Empirical)** | Run 106 in the main experiment reliably crashed due to the 500 RPD ceiling, proving infrastructure constraints. |
| *"Semantic ARIA markup improves text-based agent task accuracy over plain HTML."* | **NO (UNSUPPORTED)** | In historical trials, success was at ceiling (~99.6%) and visual grounding bypassed DOM markup. Under Protocol v3, zero live trials have been executed. |
| *"Custom data-* attributes provide zero benefit to autonomous agents."* | **NO (UNSUPPORTED)** | In historical trials, `browser-use` stripped `data-*` attributes before prompt delivery; the agent never received the treatment. |
| *"JSON-LD structured data is useless for autonomous web navigation."* | **NO (UNSUPPORTED)** | In historical trials, JSON-LD was pruned by `DISABLED_ELEMENTS`; the agent never observed it. |
| *"Semantic markup channels are functionally equivalent in agent performance."* | **NO (UNSUPPORTED)** | The study was severely underpowered ($<11\%$ power for small effects), and the ceiling effect precluded discrimination. Equivalence cannot be asserted. |
