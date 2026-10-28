# REPRODUCIBILITY GUIDE: THE DOM SERIALIZATION GAP

This repository contains the complete, 100% offline-verifiable research artifacts, measurement pipelines, statistical simulations, and manuscript sources for:

> **The DOM Serialization Gap: Architectural Pruning, Information Loss, and Observation Confounds in Autonomous Browser Agents**  
> *Under Double-Blind Peer Review (IEEE Conference Format)*

All systems audit findings, direct retention measurements, solvability proofs, and statistical simulations can be reproduced from scratch on a standard host in **under 30 seconds** with **zero live API spend ($0.00 USD)**.

---

## 1. System Requirements & Setup

- **Python Version:** Python 3.11+
- **Operating System:** Platform-agnostic (verified on Windows 11, macOS, and Linux)
- **External Dependencies:** Standard library + `pypdf`, `playwright` (optional, for browser extraction), `scipy` (optional)
- **API Keys / Paid Services:** **None required.** All analyses, measurements, and tests run 100% offline.

To set up an environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 2. Quickstart: Full Regression Test Suite (207 Tests, ~22s)

Execute the comprehensive automated test suite validating all DOM parsing mechanics, statistical estimators, data provenance ledgers, and manuscript consistency:

```bash
python -m unittest discover -s . -p "test_*.py"
```

**Expected Terminal Output:**
```text
...................................................................................
----------------------------------------------------------------------
Ran 207 tests in ~22s

OK
```

---

## 3. Step-by-Step Reproduction of Individual Core Findings

### 3.1. Direct Information Loss & Version Drift Audit (Phase 9)
Evaluates stage-by-stage metadata retention across 44 atomic target entities and six PyPI binary wheels (v0.1.0 to v0.13.11):

```bash
python phase9_execute.py
```

**Outputs Generated:**
- `INFORMATION_LOSS_MEASUREMENTS.csv`: Full entity-by-entity retention ledger with exact Clopper-Pearson 95% binomial confidence intervals.
- `INFORMATION_LOSS_MEASUREMENTS.md`: Detailed retention report across all five pipeline stages.
- `VERSION_DRIFT_AUDIT.md`: Wheel inspection report verifying immutable `DISABLED_ELEMENTS` invariants across six releases.
- `SOLVABILITY_ANALYSIS.md`: Deterministic scripted oracle solvability analysis proving $p=1.0$ on rendered typography vs $p=0.5$ on container ARIA.

### 3.2. Clean-Room Monte Carlo Power & Sample Size Simulation (Phase 7)
Executes clean-room Monte Carlo simulations ($B=10\,000$ iterations, seed 42) computing stratified risk differences using Cochran-Mantel-Haenszel weighting with Sato (1989) and Greenland-Robins (1985) variance estimators:

```bash
python phase7_execute.py
```

**Key Verified Output Metrics:**
- 3-Arm Design Power for $\Delta=0.20$ ($\alpha_{\mathrm{adj}}=0.0167$): **7.5%** (pooled baseline: **11.5%**)
- 3-Arm Design Power for $\Delta=0.35$ ($\alpha_{\mathrm{adj}}=0.0167$): **32.3%** (pooled baseline: **48.5%**)
- Required Sample Size for 80% Power ($\Delta=0.20$): $n=97\text{--}125$/arm ($N = \mathbf{291\text{--}375}$ total)
- TOST Equivalence Sample Size ($\delta_{\mathrm{equiv}} = \pm 0.10$): $N = \mathbf{825\text{--}1\,080}$ total

### 3.3. Forensic Trace Reconciliation & Provenance Ledger (Phase 6)
Reconciles all historical execution logs and disk traces into a single clean-room accounting ledger:

```bash
python phase6_execute.py
```

**Key Verified Ledger Metrics:**
- Total trace files on disk: **46 files**
- Primary eligible trials: **39 runs** (13 per arm across 5 task strata)
- Sensitivity eligible trials: **41 runs** (includes 2 non-critical boundary variants)
- Quarantined / diagnostic attempts: **4 runs** (diagnostic indices 34, 38)
- Excluded infrastructure aborts: **3 runs** (HTTP 503 upstream gateway errors)
- Classified records in `EVIDENCE_CLASS_LEDGER.csv`: **72 historical records**

### 3.4. Citation Key & BibTeX Integrity Audit (Phase 13)
Verifies that every citation in `research_paper_final.tex` resolves to a valid entry in `references.bib`:

```bash
python audit_citation_keys.py
```

**Expected Output:**
```text
Citation Key Audit Complete: Status = PASS
  Total Citations: 33
  Unique Cited Keys: 25
  Total Bib Entries: 26
  Undefined Citations: 0
  Duplicate Keys: 0
  Syntax Errors: 0
```

---

## 4. Manuscript Compilation (LaTeX to PDF)

The manuscript is authored in standard IEEE conference format (`IEEEtran.cls`).

### Compiling Locally:
```bash
pdflatex research_paper_final.tex
bibtex research_paper_final
pdflatex research_paper_final.tex
pdflatex research_paper_final.tex
```

### Compiling on Overleaf / TeX Live 2026:
1. Upload `research_paper_final.tex` and `references.bib` to a new Overleaf project.
2. Select compiler: `pdfLaTeX` (TeX Live 2026).
3. Set main document: `research_paper_final.tex`.
4. Compile: 0 errors, 0 undefined citations (`[?]`), 0 undefined references (`??`).

---

## 5. Repository Structure & Key File Map

```text
research_execution_20261018/
├── research_paper_final.tex          # Authoritative manuscript source (IEEEtran format)
├── references.bib                    # Audited BibTeX bibliography (26 entries, 0 duplicates)
├── design.json                       # Authoritative single source of experimental design parameters
├── claims_registry.json              # Canonical claims boundary registry and banned phrase list
├── RECOVERY_STATE.json               # Machine-readable recovery phase tracker (Phases 0–17)
├── RECOVERY_LOG.md                   # Append-only chronological audit log
├── RECOVERY_ISSUE_REGISTER.csv       # Disposition register for all 33 tracked issues (100% Fixed-and-verified)
├── CLAIM_EVIDENCE_MAPPING.md         # Traceability matrix mapping claims CLM-01--CLM-12 to evidence
├── MANUSCRIPT_REVISION_CHANGELOG.md  # Detailed changelog of old text -> new text transformations
├── FINAL_BUILD_LOG.txt               # Multi-pass LaTeX build verification log
├── PDF_VISUAL_QA.md                  # Layout, typography, and float barrier QA report
├── FINAL_VERIFICATION_REPORT.md      # Adversarial reviewer report and final sign-off
├── FINAL_RECOVERY_REPORT.md          # Comprehensive 17-phase recovery report
├── README_REPRODUCE.md               # This reproducibility guide
├── INFORMATION_LOSS_MEASUREMENTS.csv # Stage-by-stage retention data across 44 target entities
├── RUN_ACCOUNTING_RECONCILIATION.csv # 77-row reconciled execution ledger
├── EVIDENCE_CLASS_LEDGER.csv         # Provenance classification of all historical records (E1–E7)
├── fixtures/                         # 7 controlled HTML test fixtures
├── results/                          # Raw trace files and summary CSVs
└── test_*.py                         # 27 offline test modules (207 passing unit tests)
```
