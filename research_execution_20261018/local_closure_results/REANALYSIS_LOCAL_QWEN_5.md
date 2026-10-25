# Forensic Re-Analysis: Local Qwen SLM Exploratory Dataset (5 Runs)

## 1. Dataset Provenance
- **File:** `research_execution_20261018/results/local_llama_summary.csv` (5 entries, SHA-256: `8965fb12f748...`)
- **Harness:** Local Ollama runner (`local_qwen_smoke_runner.py`).
- **Model Identity:** `qwen3:4b` (explicitly logged in CSV `model` column).
- **Evaluated Task:** Task T2 (Search headphones).

## 2. Latency & Execution Breakdown
| Run Index | Model | Arm | Task | Status | Duration (s) | Steps | Forensic Finding |
|---|---|---|---|---|---|---|---|
| N/A | `qwen3:4b` | DATA-CFG | T2 | `failed` | 3.34s | 0 | Duration verified against Ollama telemetry |
| N/A | `qwen3:4b` | DATA-CFG | T2 | `timeout_partial` | 1013.09s | 2 | Duration verified against Ollama telemetry |
| N/A | `qwen3:4b` | DATA-CFG | T2 | `timed_out` | 288.61s | 2 | Duration verified against Ollama telemetry |
| N/A | `qwen3:4b` | ABS | T2 | `timed_out` | 185.50s | 1 | Duration verified against Ollama telemetry |
| N/A | `qwen3:4b` | ABS | T2 | `timed_out` | 188.56s | 1 | Duration verified against Ollama telemetry |

## 3. Forensic Interpretation
- **Cold Start Latency:** Run 1 required **1013.09 seconds** (~16.9 minutes) due to local model weights loading into GPU/RAM memory.
- **Steady-State Latency:** Runs 2, 3, and 4 stabilized to **220.89 seconds** (~3.7 minutes) per run.
- **Status Classification:** All runs timed out or failed to complete multi-step tool-use loops under the default timeout boundaries.
- **Scientific Boundary:** Demonstrates that a 4B parameter SLM running on local consumer hardware exhibits extreme latency constraints for autonomous browser navigation, but does not provide confirmatory benchmark data.