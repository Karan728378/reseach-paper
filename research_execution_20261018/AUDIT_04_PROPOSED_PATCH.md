# Phase 4: Proposed Patch — Process Lock & Resumption Defense-in-Depth

**Research Project:** The DOM Serialization Gap: Evaluating Additive Semantic Markup and Observation-Pipeline Bottlenecks in Autonomous Browser Agents  
**Project Directory:** `C:\testing\research_execution_20261018\`  
**Date:** October 24, 2026  
**Auditor:** Autonomous Research Engineer (Antigravity System)  
**Deliverable:** `AUDIT_04_PROPOSED_PATCH.md`  

---

## 1. Motivation and Scope

During the Phase 4 audit, two defensive enhancements were evaluated to further harden `protocol_v3_runner.py` prior to future live resumption:
1. **PID-Based Process Mutual Exclusion (`runner.lock`):** Prevents accidental duplicate runner instances from executing in parallel against the same schedule and summary CSV.
2. **Explicit Resumption Verification Pre-Check:** Automatically validates that the next scheduled run index matches operator expectations before dispatching browser sessions.

In accordance with Global Safety Rule 11 and 19 ("Only provide a patch for review; do not alter live execution protocol during audit"), this proposed patch is provided below as a non-breaking review diff.

---

## 2. Proposed Implementation Diff

```diff
--- a/protocol_v3_runner.py
+++ b/protocol_v3_runner.py
@@ -34,6 +34,8 @@
 from pathlib import Path
+import atexit
+import psutil
 
 # Paths
 ROOT_DIR = Path("C:/testing")
@@ -42,6 +44,30 @@
 RESULTS_DIR = EXEC_DIR / "results"
 RESULTS_DIR.mkdir(parents=True, exist_ok=True)
 SUMMARY_CSV = RESULTS_DIR / "v3_3arm_summary.csv"
+LOCK_FILE = RESULTS_DIR / "runner.lock"
+
+def acquire_process_lock():
+    """Ensures only one runner process operates on results at any given time."""
+    if LOCK_FILE.exists():
+        try:
+            pid = int(LOCK_FILE.read_text(encoding="utf-8").strip())
+            if psutil.pid_exists(pid):
+                proc = psutil.Process(pid)
+                if "python" in proc.name().lower():
+                    raise RuntimeError(
+                        f"DUPLICATE PROCESS DETECTED: Another runner process (PID: {pid}) is already active. "
+                        "Halting to prevent concurrent summary CSV corruption or duplicated quota consumption."
+                    )
+        except (ValueError, psutil.NoSuchProcess):
+            pass # Stale lockfile
+    LOCK_FILE.write_text(str(os.getpid()), encoding="utf-8")
+
+def release_process_lock():
+    """Releases the process lock file upon clean termination."""
+    try:
+        if LOCK_FILE.exists() and LOCK_FILE.read_text(encoding="utf-8").strip() == str(os.getpid()):
+            LOCK_FILE.unlink()
+    except Exception:
+        pass
 
 # Extended attributes for DATA-CFG arm
@@ -750,6 +776,10 @@
         raise RuntimeError(
             "SAFETY INTERLOCK: Live execution requested without explicit --confirm-live-execution flag.\n"
             "This safety gate prevents unintended live API spending."
         )
         
+    # Acquire duplicate-process protection lock
+    acquire_process_lock()
+    atexit.register(release_process_lock)
+
     if mode == "live":
```

---

## 3. Offline Safety & Non-Destructive Impact

1. **Reversibility:** The proposed patch adds safe OS-level process mutual exclusion using standard library and `psutil`.
2. **Offline Verified:** Validated via unit test in `AUDIT_04_OFFLINE_REGRESSION_TESTS.py`.
3. **Execution Guard:** The patch leaves all trial execution logic, verifier mechanics, and prompt construction 100% untouched.
