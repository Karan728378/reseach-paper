# SUBMISSION PACKAGE INTEGRITY AND VERIFICATION REPORT

**Submission Archive:** `manuscript_submission_bundle_corrected.zip`  
**Archive File Size:** 816,913 bytes  
**Archive SHA-256 Checksum:** `f82a7adbd1eeec6f26e5206576982cb12daeb8d560f3bd4b2493adfc568d01e0`  
**Host Workspace:** `C:\testing\research_execution_20261018`  
**Packaging Date:** 2026-10-25T03:07:45+05:30  
**Integrity Status:** **100% VERIFIED (0 Corrupt Files, Exact Checksum Match)**  

---

## 1. Archive Manifest & Individual File Checksums

The submission bundle was compiled directly from verified, working-tree files using `scratch/build_submission_zip.py`. Every file was cryptographically verified prior to inclusion and verified via round-trip extraction:

| File Name in Archive | Size (Bytes) | SHA-256 Checksum | Category / Purpose |
| :--- | :---: | :--- | :--- |
| `research_paper_final.tex` | 47,418 | `607f78f17e814d3b6fbf5d614828f731c36b414f48b9f1d0549079f4857b6f38` | Primary LaTeX manuscript source |
| `architecture_pipeline_figure.tex` | 5,422 | `096a646a2c6f5001764cfc25f4fc3485b367def2c8ad1dd51445b7e3e16d198f` | Standalone TikZ architecture figure |
| `references.bib` | 8,112 | `1d81070d9a243ba450e1aa04ae989602a64010a3c94f0e49bb2aa5a6cfecfe73` | Complete BibTeX bibliography (22 entries) |
| `compiled_manuscript.pdf` | 752,110 | `4ecc0ae58392aae8e701d4a441caf89bdb79d77d4ddbf6fb46f1a10691248802` | Rendered 15-page manuscript PDF |
| `README_OVERLEAF.md` | 3,409 | `0c0e2df863d80b435ee91c5ca4c15e81d7f4be4707833501a3cf841d13dbbbab` | Overleaf / TeX Live compilation guide |
| `README_SUBMISSION.txt` | 1,787 | `a491b6f470a7b45cae76f5f3e05417ae4179344445859d0267c7e9bb74f37807` | Submission manifest & instructions |
| `EVIDENCE_TO_CLAIM_MATRIX.csv` | 9,672 | `f761339b7933fef770007fe8f075d68aa7ca706852bb05527a20cbb76269661f` | Claim-by-claim forensic evidence matrix |
| `CLAIM_PROVENANCE_AUDIT.md` | 12,081 | `f66cb50ffcff12530113c23a63eb6635eb8447ec151241512df8e9834220ecdc` | In-depth textual & evidentiary provenance |
| `MODEL_RUN_PROVENANCE_AUDIT.md` | 6,005 | `e0f28fbe3feae38308cc175e11f77b7aa81395fc0245084931a2fb60a1789c62` | Model names, run counts, and latencies |
| `POWER_ANALYSIS_REPRODUCTION.md` | 3,694 | `4771316d2756d11f951f22ba549e3bf3249767fba0b92552ebc68f23cc767353` | Monte Carlo power curve reproduction |
| `TOST_SAMPLE_SIZE_AUDIT.md` | 4,660 | `02533a8b278b19163286f059296e8557ea78347209794eb8ecb21495c026e7b1` | Equivalence sample size derivations |
| `CLUSTERING_AND_EXPERIMENTAL_UNIT_AUDIT.md` | 4,400 | `9f1da63020aa70164c92ee958468d6d37fcfdb24d4529dbf170f44ecad935c75` | Kish design effect & clustering models |
| `INTERVALS_MULTIPLICITY_AND_ESTIMANDS_AUDIT.md` | 5,134 | `5efb99af9859f5f5fc8fdb9e2e5c8e317e0892ccbc1b84f2e0828591efb88232` | Wilson, Newcombe, and CMH bounds |
| `DOM_OBSERVATION_CHANNEL_AUDIT.md` | 5,854 | `1c03b5ac7e74fe1dbcf66e51187d90390a1f732b1ba42861eefc161864b971a9` | DOM observation channel funnel |
| `ACCESSIBILITY_CORRESPONDENCE_AUDIT.md` | 5,609 | `5b46c74e1998596041071d05aa6b5790be6e13b865cbef64f43477174db26a1d` | Forensic audit of 27/34 correspondence |
| `TOOL_REACHABILITY_AND_OBSERVATION_LIMITS.md` | 4,349 | `c840b2e9d32e92c22976b92be653f81525aa17537eec9cb558ea36a0d2f09dd5` | Observation omission vs. tool reachability |
| `CROSS_FRAMEWORK_FEASIBILITY_AUDIT.md` | 5,083 | `7e4f8107af54a2db65c5cbe8ba90a2a4b86b46ef32a4e21a5cf8733dff635b75` | Cross-framework architectural comparison |
| `FUTURE_BEHAVIORAL_EXPERIMENT.md` | 9,962 | `a1514cdbc9f2c8d28122d103b41d2f831b7eeb789c6d482618991a0a5dc4be91` | Unexecuted Protocol v4 RCBD specification |
| `protocol_v4_rcbd_metadata.json` | 2,315 | `b0af4831b3c2bb0e29b1cfc7c8fe77cb2d8816c21e67041f71dfc8a77a949f57` | Machine-readable protocol metadata |
| `TEST_COVERAGE_AND_REPAIR_LOG.md` | 5,297 | `245b154cbbcb20172eaec3d8339833cb5febeaf3d9aa84102c770d10b77b7aa8` | Automated test suite execution & repairs |
| `INDEPENDENT_FINAL_VALIDATION.md` | 5,537 | `7d6c0785ecd5888e99ce5b80931215112fafe7b3a017e82e3b2e72e0915f0dcb` | Independent validation pass outcomes |
| `MANUSCRIPT_REVISION_CHANGELOG.md` | 5,786 | `d2be21f782c9bf1f64aa9c8dff7413665792945d8b85773173d6e5c54432a1eb` | Comprehensive changelog of manuscript edits |
| `LATEX_AND_PDF_VALIDATION.md` | 5,396 | `eaabb0122f201e74f836932402dd1fdfb0c79be2513f59ceaafead7cc40da681` | LaTeX preflight and visual inspection pass |
| `REPRODUCIBILITY_GUIDE.md` | 8,235 | `4dbb098fa5ba9da065bb8938bf5e347e3a9fa939e602283ea8be089b02ff676e` | End-to-end reproducible offline instructions |

---

## 2. Packaging Invariants & Security Audit

1. **Exclusions Strictly Enforced:**
   - Zero virtual environment directories (`.venv311` omitted).
   - Zero cache files (`__pycache__`, `.pytest_cache` omitted).
   - Zero secrets, API keys, or operational tokens.
   - Zero temporary git objects or system files (`.git`, `.DS_Store`, `Thumbs.db` omitted).
2. **Round-Trip Integrity Test:**
   - Archive was re-opened programmatically using Python's `zipfile.testzip()`.
   - Every file was extracted in-memory and its SHA-256 hash matched against disk records with 100% precision.
