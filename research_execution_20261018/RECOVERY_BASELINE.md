# RECOVERY BASELINE AND ENVIRONMENT REPORT
**Date (UTC):** 2026-10-27T13:43:08.671555+00:00  
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
- **Total Non-Excluded Files:** 759
- **Excluded Directories:** `.venv311`, `__pycache__`, `.pytest_cache`, `.git`
- **Total Backup Size:** 25.46 MB

### Breakdown by Category
| Category | File Count | Description / Notes |
|---|---|---|
| `analysis_outputs` | 94 | Classified according to Phase 1 rules |
| `backups` | 72 | Classified according to Phase 1 rules |
| `bibliography` | 6 | Classified according to Phase 1 rules |
| `bundles` | 4 | Classified according to Phase 1 rules |
| `fixtures` | 18 | Classified according to Phase 1 rules |
| `ledgers` | 10 | Classified according to Phase 1 rules |
| `manuscript` | 14 | Classified according to Phase 1 rules |
| `other` | 40 | Classified according to Phase 1 rules |
| `raw_traces` | 69 | Classified according to Phase 1 rules |
| `reports` | 289 | Classified according to Phase 1 rules |
| `secrets` | 3 | Classified according to Phase 1 rules |
| `source_scripts` | 107 | Classified according to Phase 1 rules |
| `test` | 33 | Classified according to Phase 1 rules |

---

## 3. Authoritative Manuscript Selection
- **Authoritative TeX Source:** `research_paper_final.tex`
  - Size: `C:\testing\research_execution_20261018\research_paper_final.tex` (32760 bytes)
  - SHA-256: `04dd7c351cd4d50daa3a3934f78687b652507e811088e0e597f32884f5b13bfc`
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
| `design.json` | `09ceb1c88c5b9cd9...` | `09ceb1c88c5b9cd9...` | MATCH |
| `audit_outputs/aria_baseline_prompt_pairs.csv` | `9356e30079295471...` | `9356e30079295471...` | MATCH |
| `claims_registry.json` | `a07766529332a8b9...` | `a07766529332a8b9...` | MATCH |
| `FINAL_EXECUTION_DECISION.md` | `eaa9e2d45841e494...` | `eaa9e2d45841e494...` | MATCH |
| `scratch/inspect_raw_results.py` | `c0d516e2aa66fc22...` | `c0d516e2aa66fc22...` | MATCH |
| `final_closure_v3/references.bib` | `181f996e7a4fb7b1...` | `181f996e7a4fb7b1...` | MATCH |
| `REMEDIATION_09_REFERENCE_AUDIT.csv` | `a29792f3c91c3ff5...` | `a29792f3c91c3ff5...` | MATCH |
| `backups/backup_remediation_20261026_2028/protocol_v3_runner.py` | `db24c180e92c7cd9...` | `db24c180e92c7cd9...` | MATCH |
| `FINAL_VALIDATION_05_PROVENANCE_AND_CLAIM_MAP.csv` | `a9bec523923932ef...` | `a9bec523923932ef...` | MATCH |
| `AUDIT_04_PROPOSED_PATCH.md` | `027b03b6b50f134b...` | `027b03b6b50f134b...` | MATCH |
| `audit_20261022_final/BASELINE_VERIFICATION.md` | `083502dd0624dd5d...` | `083502dd0624dd5d...` | MATCH |
| `results/demo_live_browser_runs.csv` | `ec50f82cac34122b...` | `ec50f82cac34122b...` | MATCH |
| `research_paper.tex` | `4e43bf5cc3c0485d...` | `4e43bf5cc3c0485d...` | MATCH |
| `research_paper.pdf` | `b6d78be2a3fb57a2...` | `b6d78be2a3fb57a2...` | MATCH |
| `scratch/audit_main_147.py` | `9f7466eeaf202aa3...` | `9f7466eeaf202aa3...` | MATCH |
| `audit_metadata_reachability.py` | `4d23ed47edeb56fa...` | `4d23ed47edeb56fa...` | MATCH |
| `backups/backup_phase0_20261026_1958/daily_quota_ledger.json` | `7fa33f949501128f...` | `7fa33f949501128f...` | MATCH |
| `treatment_matrix.csv` | `3032c13878dccbd2...` | `3032c13878dccbd2...` | MATCH |
| `research_paper_final.tex.bak_phase2_20261025` | `19068ab573c2f203...` | `19068ab573c2f203...` | MATCH |
| `FINAL_ZERO_SPEND_DECISION.md` | `d23732c541fedd05...` | `d23732c541fedd05...` | MATCH |

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
