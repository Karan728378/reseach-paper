# FINAL CLAIM LIMITATIONS & BOUNDING DOCUMENT
**Project:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents  
**Scope:** Formal Disclosure of Unsupported, Bounded, and Exploratory Claims  
**Date:** 2026-10-25  

---

## 1. Non-Claims: What This Paper Does NOT Claim

To maintain absolute scientific integrity, the following negative assertions are formally documented:

1. **No Proof of General Autonomous Agent Task Success Differences:**
   - The paper does **not** claim that DOM serialization enhancements (such as exposing custom `data-*` attributes) improve autonomous agent task success rates in general web environments.
   - Historical live-model trials exhibited either acute ceiling effects (41/41 runs succeeded across all arms in the cloud pilot) or infrastructure failures (42 consecutive CDP browser drops in the 147-run main experiment).
   - Zero live-agent runs were executed under the confirmatory 72-run randomized complete block design (RCBD) protocol.
2. **No Treatment Equivalence Between Observation Formats:**
   - Because the 41-run cloud pilot achieved 100% success across all arms ($RD = 0.00$), the observed data cannot distinguish between treatment equivalence and a task battery that was insufficiently sensitive to detect observation differences.
   - Formal two one-sided tests (TOST) equivalence testing requires $N \ge 1,440$ trials ($\delta = \pm 0.10$ at $p = 0.70$), which remains unexecuted.
3. **No External Preregistration:**
   - The 72-run 3-arm and 96-run 4-arm experimental protocols are version-controlled internally in Git, but were **not** preregistered on third-party registries (e.g., Open Science Framework or AsPredicted). No claim of independent pre-experimental preregistration is made.
4. **No Universal Generalization Across Web Frameworks or Arbitrary Sites:**
   - The systems audit specifically investigates `browser-use 0.13.10` and Chromium Blink on four routes of the TechMart fixture application.
   - While the architectural mechanism (`DISABLED_ELEMENTS`, container attribute stripping, and small-icon bounding box heuristics) is inherent to the framework's source code, quantitative correspondence rates ($79.4\%$ to $100\%$) depend on page layout, CSS styling, and the presence of small non-interactive badges.
5. **No Fresh Local PDF Compilation:**
   - Because no LaTeX compiler (`pdflatex`, `xelatex`, `tectonic`) exists in the local Windows environment, `compiled_manuscript.pdf` is disclosed as a pre-existing compiled artifact, potentially stale compared to the latest LaTeX source.

---

## 2. Reconciled Data Limitations and Historical Confounders

### A. Raw Pilot (261 Rows) vs. Cleaned Pilot (250 Rows)
- **Raw Pilot:** 261 attempted trials with 251 successes (96.17%).
- **Cleaned Pilot:** 250 trials with 249 successes (99.60%).
- **Post-Hoc Selection Bias:** Exactly 11 trials were excluded: 9 failed trials from Replicate 9 and 2 extra successful trials from Replicate 1.
- **Scientific Status:** The 250-row cleaned pilot cannot be presented as independent or unbiased confirmatory evidence. It represents exploratory calibration data reflecting post-hoc survivor filtering.

### B. Main Experiment (147 Rows)
- **Phase 1 (Runs 1–105):** 105/105 completed successes (100.0% ceiling).
- **Phase 2 (Runs 106–147):** 42 consecutive failures (0/42).
- **Confounder:** All 42 failures occurred following an unrecovered Chrome DevTools Protocol (CDP) browser disconnect. The agent received empty DOM trees (`read_state_metadata == EMPTY`), iterated through 7 empty steps in ~9.12 seconds, and terminated with partial credit 0.25 from a flawed verifier.
- **Scientific Status:** These 42 runs represent infrastructure failures, not language model reasoning failures. They cannot be pooled with earlier trials or cited as evidence of agent task degradation.

### C. Cloud Pilot (41 Completed Runs / 44 Execution Attempts)
- **Task Success:** 13 ABS, 13 ARIA, 15 DATA-CFG $\rightarrow$ 100% success across all arms.
- **Harness Stability:** Run 26 encountered 3 transient HTTP 503 UNAVAILABLE errors before succeeding on attempt 4.
- **Scientific Status:** Demonstrates harness execution stability and retry resilience, but zero sample variance prevents hypothesis testing for treatment differentiation.

### D. Local Qwen Telemetry (5 Runs)
- **Telemetry:** Five exploratory diagnostic runs on laptop GPU hardware (AMD Ryzen 5 5600H, RTX 3050).
- **Durations:** `[3.34s, 1013.09s, 288.61s, 185.50s, 188.56s]`.
- **Scientific Status:** Hardware and watchdog latency profiling only; zero benchmark task completions.

### E. Synthetic Benchmark Dataset (`dataset_1_valid_complete.csv`)
- **Status:** Synthetic mock data (96 rows) used exclusively to verify that the CMH and Newcombe score confidence interval software functions execute without numerical or arithmetic errors.
- **Scientific Status:** Explicitly synthetic; not empirical agent evidence.

---

## 3. Supported and Verified Scope

The manuscript is strictly bounded and supported as an **empirical systems audit**:
1. **Source Code Proof:** Exact mechanism of element pruning (`DISABLED_ELEMENTS`), container tag flattening (lines 1046–1058), and attribute whitelist filtering (`DEFAULT_INCLUDE_ATTRIBUTES`) in `browser-use 0.13.10`.
2. **Reproducible Local Browser Evidence:** Geometry heuristic boundaries ($10 \le w, h \le 50\text{px}$), badge false positives, and multi-route correspondence census across four routes in Chromium.
3. **Action-Label Co-Location Confound:** Forensic demonstration that embedding target entity strings inside button accessible names creates observation leakage.
4. **Statistical Equivalence Bounds:** Mathematical demonstration that detecting meaningful agent performance differences requires $N \ge 1,440$ trials.
