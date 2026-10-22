# 10. Blockers, Decision Gates & Next Action Roadmap

**Audit Directory:** `C:\testing\research_audit_20261015_231500`  
**Date:** 2026-10-17  
**Auditor:** Antigravity Senior Empirical Research & Reproducibility Team  

---

## 1. Remaining Project Blockers & Risk Analysis

| Blocker / Risk Item | Severity | Root Cause | Impact if Unaddressed | Recommended Resolution |
|---|---|---|---|---|
| **1. Free Tier API Quota Limits** | **HIGH** | Google Gemini Free Tier imposes a 500 requests/day per project cap. | Any batch experiment exceeding ~100 runs will trigger HTTP 429 cascades and fail. | Use a Tier-1 pay-as-you-go API key (estimated cost for 96 runs is <$0.50), or pace batch execution with quota-aware delays across multiple days. |
| **2. Construct Invalidation via Visible Text** | **RESOLVED IN PROTOCOL** | Original tasks (T1–T5) had all target facts visible in plain text. | Agents solved tasks using human UI, rendering ARIA/data-* treatments irrelevant. | Protocol v3 replaces T1–T5 with isolated fact-retrieval tasks (lot code, warranty, stock, return window). |
| **3. Flawed Verifier Logic** | **RESOLVED IN OFFLINE SUITE** | T3 accepted 6 SKUs; T4 gave 0.25 unconditional points; T5 passed empty cart. | Corrupted accuracy scores and false-positive completions. | Replace buggy verifier with exact-match string/number and verified action verifiers. |
| **4. Harness DOM Pruning of Semantic Markup** | **RESOLVED IN ARCHITECTURE AUDIT** | `browser-use 0.13.10` strips `<script>` (JSON-LD) and un-whitelisted `data-*`. | Testing JSON-LD as standard web markup tests harness filtering rather than agent capability. | Restrict web-markup arms to VIS, ARIA, and DATA-CFG (with whitelist enabled). Treat JSON-LD only as an agent augmentation study. |
| **5. Arithmetic Run-Count Inconsistency** | **RESOLVED IN PROTOCOL** | Conflict between 6 conditions, 24-run blocks, and 90 runs. | Unbalanced experimental cells and invalid omnibus test statistics. | Freeze balanced 4-arm design: 6 tasks × 4 conditions × 4 blocks = **96 total runs**. |

---

## 2. Decision Gates for the Principal Investigator (User)

Before executing the live experimental run, the PI must decide on three specific gates:

1. **Gate 1: Condition Scope (4-Arm vs 6-Arm):**
   - *Option A (Recommended):* Adopt the clean 4-arm design (`ABS`, `VIS`, `ARIA`, `DATA-CFG`), testing facts delivered through verified-exposed DOM channels.
   - *Option B:* Keep 6 arms by including an exploratory Python-augmented JSON-LD hook and `DATA-DEFAULT` (which our audit proved is identical to ABS in prompt exposure).
2. **Gate 2: Target Model Selection:**
   - Confirm target model alias: `gemini-2.5-flash-lite` (or current `gemini-flash-lite-latest`).
3. **Gate 3: Execution Quota Budget:**
   - Confirm whether a paid Tier-1 billing account is available to execute the 96 runs continuously in a single ~45-minute batch, or if execution should be split across daily free-tier windows.

---

## 3. The Single Next Action Needed from the User

> **Authorize the Protocol v3 Freeze and select between Option A (clean 4-arm, 96-run design) or Option B (6-arm, 108/144-run design).**
>
> Once confirmed, the test fixtures and runner in `runner/` will be updated to Protocol v3, and the project will be fully ready for live execution whenever authorized.
