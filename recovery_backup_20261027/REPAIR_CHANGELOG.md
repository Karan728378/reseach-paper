# Experimental Engineering Repair & Staged Validation Changelog
**Project:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents  
**Timestamp:** 2026-10-24  
**Workspace:** `C:\testing\research_execution_20261018\`  

---

## 1. Overview of Modified and Created Files

| File | Status | Description | Timestamped Backup |
|---|---|---|---|
| `protocol_v3_runner.py` | **MODIFIED** | Core runner: lifecycle repair, in-flight state capture, safe extraction fallback, DATA-CFG delivery rule, traceback logging, summary filtering | `protocol_v3_runner.py.bak_master_debug_20261024_204400` |
| `test_implementation_fixes.py` | **MODIFIED** | Dynamic date handling (`datetime.now()`) and verified exclusion of aborted runs from completed indices | `test_implementation_fixes.py.bak_master_debug_20261024_205800` |
| `test_browser_lifecycle_and_recovery.py` | **CREATED** | 10-test offline regression suite covering all lifecycle failure modes, verifier ground truth, and recovery | N/A (New Test Suite) |
| `results/live_smoke_v2/` | **CREATED** | Isolated output directory preserving historical evidence in `results/smoke_runs/` read-only | N/A (New Output Directory) |

---

## 2. Forensic Engineering Interventions

### A. Core Runner Harness (`protocol_v3_runner.py`)

1. **In-Flight State Capture & Fallback (`extract_terminal_state`):**
   - Implemented `capture_browser_state_in_flight()` hooked into `on_step_end` callback and `register_done_callback`.
   - Updated `extract_terminal_state(session, fallback_state=None)`:
     - Tries live CDP evaluate. If the WebSocket has been closed by `Agent.close()`, recovers URL, title, cart, and order status directly from the last valid step capture.
     - Asynchronous calls `await page.get_url()` and `await page.get_title()` replace legacy synchronous attributes.
2. **Deterministic Verifier Scoring & Judge Deactivation:**
   - Configured `use_judge=False` in `Agent(...)`.
   - The benchmark relies strictly on ground-truth verifiers (`verify_task_t1` through `t6`). Turning off the judge LLM saves 1 LLM API call per trial and prevents judge timeouts.
3. **Safe Subprocess Lifecycle:**
   - Moved `await session.start()` inside the `try` block.
   - Enforced forceful process termination in `finally` via `await session.kill()` with `await session.stop()` fallback.
4. **Decoupled Telemetry & Sanitized Tracebacks:**
   - Separated `status` (`completed`, `infrastructure_aborted`, `failed`), `termination_reason` (`agent_completed`, `max_steps_reached`, `infrastructure_aborted`), and `verifier_result`.
   - Injected `detailed_record["error_traceback"] = sanitize_secret_leakage(traceback.format_exc())`.
5. **Strict `DATA-CFG` Treatment Delivery Rule:**
   - Enforced requirement that both action semantics (`data-action`) AND entity identification (`data-product-id` or `data-sku`) must be present in the serialized model observation for `complete_delivery=True`.
6. **Summary Filtering Survivorship Bias Correction:**
   - Corrected `get_completed_run_indices()` to strictly filter on `status == "completed"`, ensuring failed or aborted attempts remain eligible for retry.

---

### B. Offline Regression Suite (`test_browser_lifecycle_and_recovery.py`)

Constructed 10 standalone offline regression tests without external API dependencies:
1. `test_browser_startup_failure_handling`: Verifies exception trapping and cleanup when browser fails to launch.
2. `test_client_disconnect_during_terminal_extraction`: Verifies CDP reconnect logic when WebSocket is dead.
3. `test_terminal_state_capture_failure_does_not_mask_agent_completion`: Verifies preservation of `termination_reason="agent_completed"` when extraction fails.
4. `test_terminal_state_fallback_recovery_when_websocket_closed`: Verifies smooth state recovery from in-flight capture when reconnect fails.
5. `test_verifier_strict_correctness`: Ground-truth battery for T1–T6.
6. `test_cleanup_invoked_on_exception`: Ensures `session.kill()` / `session.stop()` is always invoked in `finally`.
7. `test_provider_429_503_classification`: Classifies rate limits and 503 errors as `infrastructure_aborted`.
8. `test_complete_delivery_rule_datacfg`: Enforces requirement for both `data-action` and `data-product-id`.
9. `test_duplicate_run_index_and_attempt_preservation`: Verifies creation of `run_{idx}_attempt_2.json` without overwriting attempt 1.
10. `test_preservation_of_failed_and_aborted_records`: Verifies summary persistence and retry eligibility.

---

## 3. Staged Live Smoke Execution Record

| Run Index | Arm / Task | Attempt | Outcome | Infrastructure Event & Resolution |
|---|---|---|---|---|
| **Run 1** | ABS / T1 | Attempt 1 | `infrastructure_aborted` | CDP socket severed post-run. Trapped safely; attempt 1 preserved. |
| **Run 1** | ABS / T1 | Attempt 2 | **`completed` (Score: 1.0)** | In-flight capture active. Cart extracted: SoundFlow Air 3 (`wh-001`). Verified. |
| **Run 2** | ARIA / T3 | Attempt 1 | `infrastructure_aborted` | Provider 503 capacity spike. Halted safely; attempt 1 preserved. |
| **Run 2** | ARIA / T3 | Attempt 2 | **`completed` (Score: 1.0)** | Neutral probe confirmed endpoint health. Cart extracted: BudPro Wireless X (`wh-002`). Verified. |
| **Run 3** | DATA-CFG / T5 | Attempt 1 | **`completed` (Score: 1.0)** | Precondition verified (`pre_cart_count: 1`). Post-state cart empty. Complete delivery confirmed (`data-action`, `data-product-id`). |
| **Run 4** | VIS / T6 | Attempt 1 | **`completed` (Score: 1.0)** | Negative probe. Warranty searched (0 matches), extracted ("not available"). Grounded refusal formulated without hallucination. |

---

## 4. Protocol Invariance Safeguards

All fundamental experimental parameters remain strictly preserved:
- Task instructions: Unaltered.
- Variant HTML structures (`v0-baseline`, `v2-aria`, `v3-data-attrs`): Unaltered.
- Vision confound guard: `use_vision=False` strictly active across all arms.
- Randomization & Blocking: RCBD block definitions preserved.
- Safety flags: `--live` and `--confirm-live-execution` enforced.
- Spend guard: $0.00 spend constraint maintained.
