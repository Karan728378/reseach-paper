# RECOVERY BASELINE AND ENVIRONMENT REPORT
**Date (UTC):** 2026-10-26T19:26:40.213889+00:00  
**Workspace:** `C:\testing\research_execution_20261018`  
**Backup Directory:** `C:\testing\recovery_backup_20261027` (Read-only)  
**Git Repository Root:** `C:\testing` (Branch: `main`, HEAD: `7bd17b432b196222ff1b2da449dbb0eac51c6c36`)

---

## 1. Environment Snapshot
- **Operating System:** `Windows 10 10.0.26300 (AMD64)`
- **Python Executable:** `C:\testing\.venv311\Scripts\python.exe`
- **Python Version:** `3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)]`
- **Playwright Package Version:** `Error: No module named 'playwright'`
- **Playwright Chromium Installations:** `chromium-1243, chromium_headless_shell-1243`
- **Secret Verification (Rule R2):** `groq_key.txt` -> `EXISTS (first 4 chars: 'PAST', length: 29 bytes)` (confirmed excluded from bundles and backups)

### Installed Key Package Hashes (K1 Verification)
| Module / File | Expected SHA-256 | Actual SHA-256 | Status |
|---|---|---|---|
| `browser_use/dom/serializer/serializer.py` | `6d523ff457d1f0c9...` | `6d523ff457d1f0c9...` | MATCH (Verified) |
| `browser_use/dom/views.py` | `01866ed2d9aa77ee...` | `01866ed2d9aa77ee...` | MATCH (Verified) |
| `browser_use/dom/service.py` | `43f8e087754ea9a6...` | `43f8e087754ea9a6...` | MATCH (Verified) |

---

## 2. File Inventory and Classification Summary
- **Total Non-Excluded Files:** 695
- **Excluded Directories:** `.venv311`, `__pycache__`, `.pytest_cache`, `.git`
- **Total Backup Size:** 13.00 MB

### Breakdown by Category
| Category | File Count | Description / Notes |
|---|---|---|
| `analysis_outputs` | 89 | Classified according to Phase 1 rules |
| `backups` | 72 | Classified according to Phase 1 rules |
| `bibliography` | 6 | Classified according to Phase 1 rules |
| `bundles` | 4 | Classified according to Phase 1 rules |
| `fixtures` | 17 | Classified according to Phase 1 rules |
| `ledgers` | 9 | Classified according to Phase 1 rules |
| `manuscript` | 14 | Classified according to Phase 1 rules |
| `other` | 26 | Classified according to Phase 1 rules |
| `raw_traces` | 69 | Classified according to Phase 1 rules |
| `reports` | 267 | Classified according to Phase 1 rules |
| `secrets` | 3 | Classified according to Phase 1 rules |
| `source_scripts` | 91 | Classified according to Phase 1 rules |
| `test` | 28 | Classified according to Phase 1 rules |

---

## 3. Authoritative Manuscript Selection
- **Authoritative TeX Source:** `research_paper_final.tex`
  - Size: `C:\testing\research_execution_20261018\research_paper_final.tex` (41913 bytes)
  - SHA-256: `39bb2a07eeff93c673d7823af603ab2b839eb55f9e77033031c12cc722ade025`
  - Document Class: `\documentclass[conference]{IEEEtran}`
  - Bibliography: `references.bib`
  - Figure include: `architecture_pipeline_figure.tex`
- **Older / Reference Manuscript Sources:**
  - `research_paper.tex` (Older draft)
  - `research_paper_audited.tex` (Intermediate audit stage)
  - `manuscript_submission_bundle.zip` (Existing submission package)

---

## 4. Backup Integrity Verification
- **Backup Target:** `C:\testing\recovery_backup_20261027`
- **Permissions:** All copied files set to `READ-ONLY` (`S_IREAD`).
- **Validation Sample:** 20 randomly selected files re-hashed from backup.
- **Match Rate:** 20 / 20 (100.0%)

### Sampled 20-File Verification Log
| Relative Path | Original SHA-256 | Backup SHA-256 | Status |
|---|---|---|---|
| `EXPERIMENT_AND_STATISTICS_AUDIT_V2.md` | `48c01d76dcc8b9e3...` | `48c01d76dcc8b9e3...` | MATCH |
| `audit_outputs/BASELINE_POOLING_RECONCILIATION.md` | `40f81f6ec8f7630e...` | `40f81f6ec8f7630e...` | MATCH |
| `COMBINED_AUDIT_REVIEW.txt` | `567c1bffa08c4ff7...` | `567c1bffa08c4ff7...` | MATCH |
| `final_review/analysis_plan.md` | `ef42c96fbb6ed85f...` | `ef42c96fbb6ed85f...` | MATCH |
| `STATISTICAL_AUDIT_REPORT.md` | `c0936d399ee24078...` | `c0936d399ee24078...` | MATCH |
| `FINAL_RESEARCH_READINESS_REPORT.md` | `2d6efdc6c57f3fbc...` | `2d6efdc6c57f3fbc...` | MATCH |
| `results/3arm_runs/run_004.json` | `bbf6490e9687fdc9...` | `bbf6490e9687fdc9...` | MATCH |
| `backups/backup_remediation_20261026_2028/references.bib` | `1d81070d9a249751...` | `1d81070d9a249751...` | MATCH |
| `fixtures/sentinel_fixture.html` | `184b4f4192d23647...` | `184b4f4192d23647...` | MATCH |
| `AUDIT_04_RESUME_READINESS.md` | `7c325ac5a0788112...` | `7c325ac5a0788112...` | MATCH |
| `audit_20261022_final/BUDGET_AND_COST_CONTROLS.md` | `6884f59addbd3bfb...` | `6884f59addbd3bfb...` | MATCH |
| `results/single_live_validation_20261026_runs/run_001.json` | `7658e7af8a3b47c6...` | `7658e7af8a3b47c6...` | MATCH |
| `results/3arm_runs/run_017.json` | `a0529d6b72383948...` | `a0529d6b72383948...` | MATCH |
| `results/3arm_runs/run_016.json` | `bc28d779d7ce80dd...` | `bc28d779d7ce80dd...` | MATCH |
| `scratch/inspect_all_41_traces.py` | `adc734718321e409...` | `adc734718321e409...` | MATCH |
| `audit_multi_framework_observation.py` | `71b89c7f80617282...` | `71b89c7f80617282...` | MATCH |
| `backups/backup_phase0_20261026_1958/DISAMBIGUATION_PROBES_PROTOCOL.md` | `4c272b30dabf2c6a...` | `4c272b30dabf2c6a...` | MATCH |
| `results/3arm_runs/run_026_attempt_4.json` | `5fede06877ccc6c0...` | `5fede06877ccc6c0...` | MATCH |
| `FUTURE_BEHAVIORAL_EXPERIMENT.md` | `a1514cdbc9f2d7f4...` | `a1514cdbc9f2d7f4...` | MATCH |
| `results/single_live_validation_retry_20261026_runs/run_001.json` | `a78170e74b89cb09...` | `a78170e74b89cb09...` | MATCH |

---

## 5. Pip Freeze Environment
```text
aiofiles==25.1.0
aiohappyeyeballs==2.7.1
aiohttp==3.14.3
aiosignal==1.4.0
annotated-types==0.8.0
anthropic==1.9.0
anyio==4.12.1
attrs==26.1.0
backoff==2.2.1
beautifulsoup4==4.15.0
browser-harness==0.1.13
browser-use==0.13.10
browser-use-sdk==3.4.2
bubus==1.5.6
cdp-use==1.4.5
certifi==2026.7.22
cffi==2.1.1
charset-normalizer==3.5.1
click==8.3.3
cloudpickle==3.1.2
colorama==0.4.6
cryptography==50.0.1
distro==1.9.0
docstring_parser==0.18.0
fetch-use==0.4.0
filetype==1.2.0
frozenlist==1.8.0
google-api-core==2.29.0
google-api-python-client==2.188.0
google-auth==2.59.0
google-auth-httplib2==0.4.2
google-auth-oauthlib==1.2.4
google-genai==2.25.0
googleapis-common-protos==1.75.4
groq==1.0.0
h11==0.16.0
httpcore==1.0.9
httpcore2==2.13.1
httplib2==0.32.0
httpx==0.28.1
httpx2==2.13.1
idna==3.20
inquirerpy==0.3.4
jiter==0.17.0
jsonpatch==1.33
jsonpointer==3.1.1
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
langchain-anthropic==1.7.4
langchain-core==1.6.5
langchain-google-genai==4.4.0
langchain-protocol==0.0.19
langsmith==0.14.1
lxml==6.1.3
markdown-it-py==4.2.0
markdownify==1.2.2
mcp==2.1.1
mcp-types==2.1.1
mdurl==0.1.2
multidict==6.9.1
oauthlib==4.0.0
ollama==0.6.1
openai==2.26.0
opentelemetry-api==1.45.0
orjson==3.12.0
packaging==26.3
pfzy==0.3.4
pillow==12.3.0
portalocker==4.4.0
posthog==7.7.0
prompt_toolkit==3.0.53
propcache==0.5.4
proto-plus==1.28.4
protobuf==6.33.6
psutil==7.2.2
pyasn1==0.6.4
pyasn1_modules==0.4.2
pycparser==3.0
pydantic==2.13.5
pydantic-settings==2.15.0
pydantic_core==2.46.5
Pygments==2.21.0
PyJWT==2.15.1
pyotp==2.9.0
pyparsing==3.3.3
pypdf==6.16.2
python-dateutil==2.9.0.post0
python-docx==1.2.0
python-dotenv==1.2.2
python-multipart==0.0.32
pywin32==312
PyYAML==6.0.3
referencing==0.37.0
reportlab==4.4.9
requests==2.33.0
requests-oauthlib==2.0.0
requests-toolbelt==1.0.0
rich==14.3.3
rpds-py==2026.6.3
rsa==4.9.1
screeninfo==0.8.1
six==1.17.0
sniffio==1.3.1
soupsieve==2.10
sse-starlette==3.5.0
starlette==1.7.0
tenacity==9.1.4
tqdm==4.70.1
truststore==0.10.4
typing-inspection==0.4.4
typing_extensions==4.15.0
uritemplate==4.2.0
urllib3==2.8.0
uuid7==0.1.0
uuid_utils==0.17.1
uvicorn==0.54.0
wcwidth==0.9.1
websockets==15.0.1
xxhash==4.0.1
yarl==1.25.1
zstandard==0.25.0
```
