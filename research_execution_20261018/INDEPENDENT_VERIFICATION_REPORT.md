# INDEPENDENT RESEARCH VERIFICATION REPORT (PHASE 1)

**Project:** *The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents*  
**Auditor:** Independent Senior Research Verification Auditor  
**Host Workspace:** `C:\testing\research_execution_20261018`  
**Python Runtime:** `C:\testing\.venv311\Scripts\python.exe` (Python 3.11.9)  
**Audit Date (UTC):** 2026-10-27  
**Git Baseline Commit:** `7bd17b4 feat(research): complete Phase A-G local experiments, multi-route census, geometry boundary audit, and claim matrix`  

---

## 1. Real Current State & Environmental Inventory

### 1.1 Git Status & Workspace Hygiene
- **Branch:** `master`
- **Head Commit:** `7bd17b4`
- **Working Tree State:** Workspace contains uncommitted recovery artifacts, test scripts, reconciled ledgers, and generated verification reports. All raw logs and historical data in `results/` are preserved intact.

### 1.2 Issue Count Discrepancy Resolution (33 vs 34 Issues)
- **Discrepancy Documented:** Prior audit reports alternately cited "33 issues" and "34 issues".
- **Forensic Code & Register Trace:**
  - File: `RECOVERY_ISSUE_REGISTER.csv`
  - Total text lines in file: **34 lines**
  - Header line: `id,root_id,source,severity,location,evidence_available,evidence_required,proposed_correction,requires_live,status,impl_status,verif_cmd,verif_result,affected`
  - Data rows: Exactly **33 rows**
  - Issue ID breakdown:
    - 15 `K`-series issues: `K1` through `K15` (15 issues)
    - 18 `C`-series issues: `C1` through `C18` (18 issues)
    - Sum: $15 + 18 = \mathbf{33\text{ registered issues}}$.
- **Root Cause of Divergence:** Scripts executing `len(f.readlines())` reported `34` (counting the CSV header row as an issue), whereas CSV parsing scripts iterating over data rows reported `33` (`len(data_rows)`).
- **Authoritative Resolution:** The project tracks exactly **33 substantive issues** (all 33 are independently verified with status `Fixed-and-verified`).

### 1.3 Key Input & Output Cryptographic Hash Inventory

| File Path | Size (Bytes) | SHA-256 Digest | Provenance & Role |
| :--- | :---: | :--- | :--- |
| `research_paper_final.tex` | 32,760 | `0144fbb7cfadcf6c6d0fa73bc5b4430eefb18c64267cecf2630656a1b24bf4a0` | Authoritative manuscript source (198-word abstract) |
| `references.bib` | 6,346 | `86801867c2957b4943fcfd5c41e8bb7aa60ffbf061e89cf0aa04ba3f0a59a72b` | Audited BibTeX database (26 entries, 0 errors) |
| `design.json` | 2,060 | `47f3ca697c1d76371dd2da58525b682e01dfdb6a40a8d67c9d57a2f58e5f3aa5` | Single source of truth for 3-arm RCBD parameters |
| `claims_registry.json` | 3,041 | `4f38be0e35327ecae53a544c207593c200787e9ec88439df48a58f7976e3ccbe` | Authoritative claim bounds and banned phrase registry |
| `RECOVERY_STATE.json` | 5,836 | `5603ca9b62fbca3a76e938928db64bb6b2e04db7328bf388a101f308f237f374` | Machine-readable recovery phase tracker |
| `RECOVERY_ISSUE_REGISTER.csv`| 17,987 | `9e54d89a6ea861a995739ce34f378d3862668dae54efcfb8ebbc90f488ddf0d1` | Master issue register (33 issues, 34 CSV lines) |
| `RUN_ACCOUNTING_RECONCILIATION.csv` | 13,018 | `132646b5a37f1947b0e11894a82200fb73315fa764510b656758414436577881` | 77-row reconciled ledger of all disk traces |
| `EVIDENCE_CLASS_LEDGER.csv` | 14,845 | `2f9d5fc9c1352a19236d934bb7d0a273b3e21e847c21142dc5ef8ce833da97e0` | Categorized provenance ledger of all 72 historical runs |
| `INFORMATION_LOSS_MEASUREMENTS.csv` | 9,997 | `519bac28a0f00728551d3620a0ea5d45ad18ce22e7f5a61e551bf8f539972c96` | 44 target entity retention measurements |
| `manuscript_submission_bundle.zip` | 8,710,504 | `a39158ff8a1a3641bf39cecae5d956550731ffba7c7f1e58285a81ca55ae101b` | Release bundle (653 files, 0 corrupted files) |

### 1.4 Dataset Counts & Provenance Classification
- **Total Tracked Historical Records:** 72 records in `EVIDENCE_CLASS_LEDGER.csv`.
- **Disk Trace Inventory (`results/3arm_runs/`):** Exactly **46 trace files** on disk.
  - Primary eligible trials: **39 runs** ($13/13$ per arm across 5 task strata).
  - Sensitivity eligible trials: **41 runs** (includes 2 variant runs).
  - Quarantined attempts: **4 runs** (duplicate index executions at indices 34 & 38).
  - Excluded infrastructure aborts: **3 runs** (HTTP 503 gateway timeouts on index 26).
- **Local Diagnostic Runs (`results/local_llama_pilot_runs/`):** **5 runs** (`qwen_diag_001` through `qwen_diag_005`), classified strictly under Evidence Class E6 (telemetry/watchdog test).
- **Oct 26 Unreported Live Runs (`results/live_single_attempt_20261026_runs/`):** **16 runs**, classified under Evidence Class E6 (diagnostic infrastructure smoke probes, not confirmatory).

### 1.5 Test Discovery & Execution Status
- Total test files on disk: 31 files.
- Files defining `unittest.TestCase` suites: **27 modules**.
- Files serving as standalone/live probe scripts: **4 files** (`test_agent_prompt_pipeline.py`, `test_format_inspection.py`, `test_groq_connection.py`, `test_single_smoke_request.py`).
- Total unit tests discovered and passing: **207 unit tests (100% passing, 0 failing, 0 skipped)** across all 27 modules in ~22 seconds.

---

## 2. Independent Claim-by-Claim Verification Matrix

| Claim ID & Summary | Source Artifact | Independent Check | Result | Evidence & Hash / Location | Remaining Limitation |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **CLM-01: Pilot Ceiling & Retraction**<br>Standard TechMart tasks are 100% solvable from visible text ($p=1.0$), creating a ceiling effect in pilot ($13/13$ per arm, exact CI $[0.7529, 1.0000]$). Sufficiency claim retracted. | `SOLVABILITY_ANALYSIS.md`, `phase9_execute.py`, `phase7_execute.py` | Non-LLM scripted oracle reader run against serialized observations; exact combinatorial binomial CDF bisection. | **VERIFIED** | Scripted oracle achieves $p=1.0$ on T1–T5; Clopper-Pearson exact inversion yields $[0.7529, 1.0000]$ for $13/13$. Upper bound failure rate is $24.71\%$. | Pilot reflects harness stability, not evidence of agent reasoning on semantic markup. |
| **CLM-02: JSON-LD Pruning**<br>Schema.org JSON-LD in `<script type="application/ld+json">` is unconditionally eliminated at Stage 2 by `DISABLED_ELEMENTS = {'style','script','head','meta','link','title'}`. | `serializer.py` L18, L481; `VERSION_DRIFT_AUDIT.md` | AST inspection of installed wheel code and verification across 6 PyPI binary wheels (v0.1.0 to v0.13.11). | **VERIFIED** | Code check confirms `DISABLED_ELEMENTS` at L18/L481. All 6 wheels verify byte-for-byte SHA-256 against PyPI registry. Stage 2 eliminates 4/4 JSON-LD entities. | Evaluated specifically on Chromium Blink DOM engine under `browser-use`. |
| **CLM-03: AXTree Circularity**<br>Selector correspondence with Blink AXTree is partially circular by construction because `ClickableElementDetector` queries `ax_node.role`. | `clickable_elements.py` L204–225; `compare_accessibility_tree.py` | Source code tracing of CDP call `Accessibility.getFullAXTree` and inspection of interactive role filtering logic. | **VERIFIED** | `ClickableElementDetector` calls `node.ax_node.role` to determine interactive inclusion. Correspondence is $27/34 = 79.4\%$ operational and $26/26 = 100\%$ leaf controls. | Applies to `browser-use` interactive detection heuristics. |
| **CLM-04: Container ARIA Interactivity Gating**<br>Container spans and divs bearing `role="region"` or `aria-label` are stripped at Stage 4 by `serializer.py` L1046–1051, emitting only inner text. | `serializer.py` L1046–1051; `test_disambiguation_probes.py` | Dynamic trace on `fixtures/disambiguation_probe_b.html` under Chromium CDP. | **VERIFIED** | Non-interactive containers bypass `_build_attributes_string()`; tag wrapper and attributes stripped; probe B rendered mathematically unsolvable ($p=0.5$). | Does not apply to leaf interactive buttons (`<button>`), where ARIA is preserved. |
| **CLM-05: 10–50px Icon Heuristic**<br>Bounding-box heuristic ($10 \le w, h \le 50$\,px) misclassifies non-interactive badge spans as interactive buttons (7 false positives for 48.6px "In Stock" badges). | `scratch/check_bounds.py`, `test_forensic_audit_regressions.py` | Boundary evaluation of computed element geometry on TechMart `#home` catalog route. | **VERIFIED** | 7 "In Stock" badges ($48.625 \times 15$\,px) satisfy $10 \le w, h \le 50$\,px and have class, triggering button emission; 1 "Out of Stock" badge ($74.766$\,px) pruned. | Specific to websites with small badge spans bearing CSS classes. |
| **CLM-06: Clean-Room Monte Carlo Power**<br>3-arm RCBD design achieves 7.5% power for $\Delta=0.20$ and 32.3% for $\Delta=0.35$ ($B=10\,000$, $\alpha_{\mathrm{adj}}=0.0167$); pooled baseline achieves 11.5% and 48.5%. | `phase7_execute.py`, `design.json` | Monte Carlo clean-room simulation ($B=10\,000$, seed 42) using Cochran-Mantel-Haenszel stratified risk differences. | **VERIFIED** | Recomputed power: 7.51% (MCSE 0.26%) for $\Delta=0.20$; 32.31% (MCSE 0.47%) for $\Delta=0.35$. Null simulation Type I error: 0.52% ($\le 1.67\%$). | Assumes constant stratum weights and binomial variance model. |
| **CLM-07: Sample Size Derivations**<br>Detecting $\Delta=0.20$ at 80% power ($\alpha_{\mathrm{adj}}=0.0167$) in 3-arm design requires $N=291\text{--}375$; TOST equivalence requires $N=825\text{--}1\,080$. | `phase7_execute.py`, `design.json` | Closed-form normal approximation with Bonferroni correction and Schuirmann TOST margins. | **VERIFIED** | Closed-form formula $n = \frac{(z_{\alpha/2} + z_\beta)^2 [p_1(1-p_1) + p_2(1-p_2)]}{\Delta^2}$ gives $n=97\text{--}125$/arm ($N=291\text{--}375$). | Sensitivity varies with baseline success rate ($p_0 \in [0.30, 0.70]$). |
| **CLM-08: Trace Accounting Reconciliation**<br>Reconciliation of all 46 trace files on disk: 39 primary eligible, 4 quarantined, 3 infrastructure aborts. | `RUN_ACCOUNTING_RECONCILIATION.csv`, `phase6_execute.py` | Scripted reconciliation matching every `.json` file in `results/3arm_runs/` against execution schedules and timestamps. | **VERIFIED** | Clean-room script verifies 46 files: 39 primary (13/arm), 4 duplicates (indices 34 & 38), 3 aborts (HTTP 503 at index 26). | None; 100% of files on disk accounted for. |
| **CLM-09: Stage 5 Prompt Interception**<br>Stage 5 prompt buffer interception was characterized offline using `MockChatModel`; live pilot logged attribute flags, not raw prompts. | `audit_metadata_reachability.py`, `results/3arm_runs/*.json` | Schema inspection of raw JSON run files and offline execution of `MockChatModel` hook. | **VERIFIED** | Raw pilot JSON records contain `treatment_attribute_observed` boolean flags; offline `MockChatModel` intercepts raw model prompts. | Historical pilot cannot retroactively recover unlogged prompt buffers. |
| **CLM-10: Out-of-Band Interfaces**<br>`/llms.txt` and MCP provide out-of-band context endpoints that bypass DOM serialization, rather than enriching HTML markup. | `references.bib`, `CITATION_AUDIT.md`, `llmstxt2024`, `mcp2024` | Review of official specifications (`llmstxt.org`, `modelcontextprotocol.io`). | **VERIFIED** | Specifications verify that `/llms.txt` is an HTTP endpoint and MCP is a JSON-RPC protocol; neither modifies HTML DOM trees. | Literature context; not a code-level implementation. |
| **CLM-11: Wheel Invariance across Releases**<br>`DISABLED_ELEMENTS` and developer attribute omission are immutable invariants across 6 releases (v0.1.0 to v0.13.11). | `VERSION_DRIFT_AUDIT.md`, `phase9_execute.py` | Download and static analysis of 6 PyPI binary distributions. | **VERIFIED** | Forensic inspection confirms `DISABLED_ELEMENTS` contains `script` and `meta` in all 6 releases. | Evaluated across officially published PyPI wheels up to v0.13.11. |
| **CLM-12: Co-Location Confound**<br>Adding metadata to an element with visible text conflates spatial reference resolution with delivery channel. | `research_paper_final.tex` Sec. V-C, `SOLVABILITY_ANALYSIS.md` | $3 \times 3$ factorial design matrix crossing Content Placement ($A_1$--$A_3$) with Channel ($B_1$--$B_3$). | **VERIFIED** | Scripted oracle proves causal contrast exists only in cell $(A_2, B_3)$, where visible typography is generic. | Methodological framework; requires confirmatory trials to measure effect size. |

---

## 3. Discrepancies Found & Corrected in Prior Reports

1. **Issue Count Discrepancy (33 vs 34):**
   - *Prior finding:* Reports inconsistently cited 33 and 34 issues.
   - *Independent Verification:* File has 34 lines total: 1 header row + exactly 33 data issue rows. Correct count is **33 substantive issues**, all Fixed-and-verified.
2. **Abstract Word Count Calibration:**
   - *Prior finding:* Abstract previously stood at 287 words, exceeding the IEEE 200-word ceiling.
   - *Independent Verification:* Current abstract measures exactly **198 words**, containing all required parameters and zero banned phrases.
3. **Power Analysis Number Alignment:**
   - *Prior finding:* Abstract previously cited obsolete power numbers ($10.8\%$ / $49.6\%$).
   - *Independent Verification:* Authoritatively updated to clean-room $B=10\,000$ CMH simulations: $7.5\%$ and $32.3\%$ for true 3-arm RCBD; $11.5\%$ and $48.5\%$ under pooled baseline.

---

## 4. Phase 1 Sign-Off

The real current state of the workspace is established, fully verified, and free of contradictions. All 12 primary scientific claims are substantiated by reproducible code and primary data.
