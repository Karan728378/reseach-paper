# OVERNIGHT BASELINE INVENTORY

**Timestamp:** 2026-10-25T02:52:00+05:30  
**Host Workspace:** `C:\testing`  
**Research Working Directory:** `C:\testing\research_execution_20261018`  
**Git Root:** `C:\testing`  
**Branch:** `main` (tracking `origin/main`)  
**Git Remote:** `https://github.com/Karan728378/reseach-paper.git`  
**Current Head Commit:** `64068ed` ("Initial commit: Research project on DOM serialization gap in autonomous browser agents, including preflight verification, offline test suite, and Protocol v4 RCBD specification")

---

## 1. System and Runtime Environment

| Component | Verified Specification | Source / Verification Method |
| :--- | :--- | :--- |
| **Operating System** | Windows 10 (Build 10.0.26300-SP0, 64-bit AMD64) | `platform.platform()` |
| **Python Runtime** | Python 3.11.9 (`C:\testing\.venv311\Scripts\python.exe`) | `sys.version` |
| **Core Framework** | `browser-use==0.13.10` | `importlib.metadata.version('browser-use')` |
| **Related Packages** | `browser-use-sdk==3.4.2`, `pydantic==2.13.5`, `langchain-core==1.6.5`, `langchain-google-genai==4.4.0` | `pip freeze` |
| **TeX Distribution** | No local TeX distribution (`pdflatex`, `xelatex`, `tectonic` absent from PATH) | `Get-Command` check |
| **PDF Compilation** | Overleaf external compiler used for artifact generation | Historical project record & `README_OVERLEAF.md` |

---

## 2. Test Suite Baseline

- **Test Discovery Command:** `& "C:\testing\.venv311\Scripts\python.exe" -m unittest discover -s . -p "test_*.py"`
- **Total Tests Discovered:** 126
- **Test Result:** `Ran 126 tests in 12.275s - OK`
- **Failures / Errors:** 0
- **Crucial Caution:** Passing 126 unit/mock tests validates software logic, mock data structures, and pipeline wiring; it does **not** constitute empirical proof that LLM agents succeed in live web browsing.

---

## 3. Quota Ledger & Experiment Stop Status

**File:** `results/daily_quota_ledger.json` (SHA-256: `7fa33f949501128f935b2c4c35da6ec8d8a296846e2a3a1e6496a54e12bb62b4`)

```json
{
  "date": "2026-10-24",
  "cumulative_requests": 604,
  "cumulative_cost_usd": 0.67044,
  "cumulative_prompt_tokens": 84000,
  "cumulative_completion_tokens": 1200,
  "runs_completed": 2,
  "model_name": "gemini-3.1-flash-lite",
  "cost_ceiling_usd": 0.0,
  "max_requests_ceiling": 600,
  "is_free_tier": true,
  "halted_due_to_ceiling": true,
  "last_updated": "2026-10-24T22:50:52.089039"
}
```

- **Halt Status:** `halted_due_to_ceiling: true`. Cumulative requests (604) exceed the configured maximum ceiling (600).
- **Execution Safety Directive:** Zero live API calls, zero cost, and zero bypass of the quota guard. All investigations must remain strictly offline, deterministic, and analytical.

---

## 4. Primary Evidence & Artifact Hashes

| File / Artifact | SHA-256 Checksum | Purpose / Content Description |
| :--- | :--- | :--- |
| `research_paper_final.tex` | `9316286ac8b6e0881a8f7f53858710fa09aa1833460b8acf1eb8b5705d69935d` | Main LaTeX manuscript source (15-page structure) |
| `references.bib` | `ab151539991ce71403793d6c3ea3d0591ed1ad8c11fd2974a8fe0a5ad00832e6` | BibTeX bibliography (verified keys, corrected Yang/Xie citations) |
| `architecture_pipeline_figure.tex` | `096a646a2c6f5001764cfc25f4fc3485b367def2c8ad1dd51445b7e3e16d198f` | Standalone TikZ architecture figure (clean tiers, no overlap) |
| `compiled_manuscript.pdf` | `4ecc0ae58392aae8e701d4a441caf89bdb79d77d4ddbf6fb46f1a10691248802` | Compiled 15-page PDF from Overleaf (timestamp 2026-10-25 02:21) |
| `manuscript_submission_bundle_corrected.zip` | `0ee80d5a8cbff4190b0773184a74067f6a2ce6443b5cdf9230b9970277ec1ee1` | Known previous submission bundle |
| `results/daily_quota_ledger.json` | `7fa33f949501128f935b2c4c35da6ec8d8a296846e2a3a1e6496a54e12bb62b4` | Quota ledger enforcing hard stop |
| `results/v3_3arm_summary.csv` | `3fe1ea364668a56f2566f1c3311cd7fbe284fef85f8ed566054e790de194e4a4` | Cloud pilot 41 completed runs (100% success ceiling) |
| `results/v3_run_summary.csv` | `6fb1290bb499710e52586311f524a1d1f3aa77a9ff4453f7d28fe617f6bf66cd` | Raw pilot runs ledger (44 total attempts, 41 successes, 3 retries) |
| `results/local_llama_summary.csv` | `8965fb12f748ca6aab77d2c61faef7056d3dcbce5de55f0cae09bca00d80f4ab` | Local Qwen exploratory sample (5 runs, timeout/cancellation telemetry) |
| `accessibility_tree_comparison.json` | `d27004bbd7ffca10099b7eaee04cf4d12689c20737e5a22af7bd928f885ea7ed` | 34 selector-map entries, 27 matched AXTree nodes, 7 stock spans |
| `offline_test_results.json` | `f9cca3a29fa54014cb6d29ec1e4346189c6788179b2e15b350fd3c54c841a2df` | Serializer offline evaluation results |
| `serialization_audit_metrics.json` | `0f1c9d903c8abba3b4a82f5dfb66caf1350dd493603bba74fdbd19fd036ce594` | Stage-by-stage token and node compression metrics |

---

## 5. Verified Facts vs. Unresolved Discrepancies

### Verified Facts
1. **DOM vs. AXTree Architecture:** In `browser-use 0.13.10`, the DOM serializer executes a custom recursive traversal of the live DOM; the Chromium AXTree is generated in parallel by Blink's accessibility subsystem. They are parallel pipelines, not sequential filtering stages.
2. **27/34 Accessibility Finding Root Cause:** The 7 unmatched elements on route `#home` are `<span class="product-stock in-stock">` across product cards 1–7. Each measures exactly $48.625\text{px} \times 15.0\text{px}$, matching the bounding box heuristic ($10 \le w, h \le 50$ with class) in `clickable_elements.py:228-240`. The 8th badge ("Out of Stock") measures $74.766\text{px}$ wide and is correctly excluded. Chromium Blink treats static text as non-interactive (`ignored: true`), omitting AXNode IDs.
3. **Dual Denominators:** Framework operational selector-map correspondence is $27/34 = 79.41\%$ ($95\%$ Wilson CI: $[63.2\%, 89.7\%]$). Semantic control correspondence is $27/27 = 100.0\%$.
4. **Cloud Pilot Ceiling Effect:** 41 completed runs achieved 100% success ($13/13$ ABS, $13/13$ ARIA, $15/15$ DATA-CFG, 3 transient retries on Run 26 resolved). Risk difference is identically $\hat{\theta} = 0.0$ due to an acute ceiling effect on simple tasks.
5. **Local Hardware Telemetry (Qwen):** 5 exploratory runs on hybrid CPU/GPU hardware (4 GB VRAM) illustrated harness timeout mechanics and watchdog cancellations (`asyncio.CancelledError`), not model reasoning scaling laws.
6. **Confirmatory Experiment:** The 4-arm randomized block confirmatory behavioral experiment remains unexecuted.

### Outstanding Discrepancies to Reconcile
1. **Model Identifiers in Pilot Logs vs. Manuscript:** Some early manuscript text mentioned `Gemini 3.1 Flash Lite` and `Gemini 2.5 Flash Lite`, while Qwen model identifiers varied between `qwen3:4b` and `qwen2.5:7b-instruct-q4_K_M`. Workstream 4 will establish the precise mapping from primary records.
2. **Power Analysis Script vs. Manuscript Text:** Power estimates (10.8%, 49.6%, 98.6% for effect sizes 0.20, 0.35, 0.70 at $N=20$) must be recomputed from actual simulation code and Monte Carlo standard errors verified.
3. **TOST Sample Size Derivation:** Formulations around $N \approx 360$ ($p=0.70$), $N \approx 429$ ($p=0.50$), and cluster-inflated $N \approx 468$ ($\text{DEFF}=1.30$) require explicit step-by-step mathematical verification.
4. **Design Effect & Clustering:** The assumed $m=4$, $\rho=0.10$ cluster size requires a formal sensitivity analysis across task/page clustering models.
