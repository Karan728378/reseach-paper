# Audit Phases A–I: Detailed Findings
**Audit Date:** 2026-10-18  |  **Mode:** Offline, Read-Only, Zero-API

---

## Phase A: File Integrity

17 key files hashed and compared against 2026-10-15 baseline manifest.

| File | Change Status |
|------|---------------|
| `index.html` | UNCHANGED |
| `runner/agent-runner.py` | UNCHANGED |
| `runner/verifier.py` | UNCHANGED |
| `runner/logger.py` | UNCHANGED |
| `runner/requirements.txt` | UNCHANGED |
| `tasks/task-definitions.json` | UNCHANGED |
| `shared/products.js` | UNCHANGED |
| `shared/app-core.js` | UNCHANGED |
| `shared/styles.css` | UNCHANGED |
| `variants/v0-baseline/index.html` | UNCHANGED |
| `variants/v1-jsonld/index.html` | UNCHANGED |
| `variants/v2-aria/index.html` | UNCHANGED |
| `variants/v3-data-attrs/index.html` | UNCHANGED |
| `variants/v4-evidence-meta/index.html` | UNCHANGED |
| `results/main_experiment/full-summary.csv` | UNCHANGED |
| `results/pilot-summary-clean.csv` | UNCHANGED |
| `results/pilot-summary.csv` | UNCHANGED |

> Full hashes in `file_integrity.csv`.

---

## Phase B: Historical Experiment Reconstruction


- **Total runs:** 147
- **Successful:** 105 (71.4%)
- **Failed:** 42
- **Quota failure onset:** Run #106 (~run index 106)
- **Runs before quota failure (valid):** 105
- **Runs after quota failure (contaminated):** 42

### Per-Variant Statistics (all 148 runs)
| Variant | N | Successes | Success Rate | Mean Steps |
|---------|---|-----------|--------------|------------|
| v0-baseline | 39 | 30 | 76.9% | 5.5 |
| v1-jsonld | 33 | 23 | 69.7% | 5.0 |
| v2-aria | 37 | 26 | 70.3% | 5.7 |
| v3-data-attrs | 38 | 26 | 68.4% | 5.4 |

> **Note:** These success rates include post-quota runs (all fail) and verifier-flawed T3/T4/T5 results. They are NOT valid for cross-arm comparisons.

---

## Phase C: browser-use Observation Pipeline

### Critical Findings
| Arm | Channel | Token Reaches LLM? | Evidence |
|-----|---------|-------------------|----------|
| ABS | Absent | No | N/A |
| VIS (v0-baseline) | Visible text | **Yes** | DOM snapshot text body |
| JSON-LD (v1-jsonld) | `<script type=application/ld+json>` | **No** | `script` in `DISABLED_ELEMENTS` |
| ARIA (v2-aria) | `aria-label` attribute | **Yes** | `aria-label` in `DEFAULT_INCLUDE_ATTRIBUTES` |
| DATA-CFG (v3-data-attrs) | `data-*` attribute | **No (default) / Yes (patched)** | Custom data-* NOT in `DEFAULT_INCLUDE_ATTRIBUTES` |
| META (v4-evidence-meta) | `<meta>` tags | **No** | `meta` in `DISABLED_ELEMENTS` |

**Source files:**
- Serializer: `C:\testing\.venv311\Lib\site-packages\browser_use\dom\serializer\serializer.py`
- Views: `C:\testing\.venv311\Lib\site-packages\browser_use\dom\views.py`

---

## Phase D: Task Definitions & Verifier Correctness

### Verifier Flaws
- **T3** (CRITICAL — inflated T3 success rates across all variants): verify_cart_state accepted wh-001 (lowest-rated) when success criterion requires wh-002 (second-highest rated). Substring check on SKU without exact-cart-only validation. [Source: `runner/verifier.py:~L350-420`]
- **T4** (MODERATE — inflated partial scores for T4 failures): verify_order_state awarded partial_score=0.25 unconditionally on failure path (checkout_reached step scored even when order not confirmed and SKU not in order). [Source: `runner/verifier.py:~L450-520`]
- **T5** (CRITICAL — T5 success in ABS/baseline could be vacuous (agent ran on already-empty cart)): verify_cart_state returned success=True on empty cart without checking that pre-seeded wh-001 was actually present before the agent ran (setup_script not verified pre-run). [Source: `runner/verifier.py:~L280-330`]

### Substring Match False Positive Risks
- **T1** (token=`36`): naive match on agent refusal text → `True` (should be False)
- **T3** (token=`43`): naive match on agent refusal text → `True` (should be False)
- **T4** (token=`45`): naive match on agent refusal text → `True` (should be False)

### Recommended Verifier Fixes
- T3: Use cart_exact_match (length==1 AND sku==wh-002) — already in task-definitions.json v2 but legacy verifier.py does not enforce it.
- T4: Remove unconditional partial credit; require window.__orderConfirmed__===true AND lastOrder.items contains mse-001.
- T5: Add pre-run JS assertion that localStorage cart contains wh-001 before agent launches.
- All retrieval tasks: Replace naive substring match with regex word-boundary match and require match only in structured final_result field, not in full agent reasoning text.

---

## Phase E: Treatment Design Evaluation

### v0-baseline (`VIS`)
- **Channel:** Visible text
- **Model Sees Token:** True
- **Via DOM Snapshot:** True
- **Via Vision:** True
- **Confounds:** Vision reinforcement if use_vision=True (dual-channel)

### v1-jsonld (`JSON-LD (BLOCKED)`)
- **Channel:** script[type=application/ld+json]
- **Model Sees Token:** False
- **Via DOM Snapshot:** False
- **Via Vision:** False
- ⚠️ **Critical Flaw:** v1-jsonld IS FUNCTIONALLY EQUIVALENT TO ABS (absent) arm for the LLM. It does NOT test JSON-LD channel effectiveness.
- **Confounds:** DISABLED_ELEMENTS prunes script tags — token NEVER reaches LLM. This arm tests hallucination, not JSON-LD delivery.

### v2-aria (`ARIA`)
- **Channel:** aria-label attribute
- **Model Sees Token:** True
- **Via DOM Snapshot:** True
- **Via Vision:** False
- **Confounds:** aria-label IS in DEFAULT_INCLUDE_ATTRIBUTES — correctly delivered.

### v3-data-attrs (`DATA (requires patch)`)
- **Channel:** data-* attribute
- **Model Sees Token:** ONLY IF include_attributes patched to add custom data-* names
- **Via DOM Snapshot:** False
- **Via Vision:** False
- ⚠️ **Critical Flaw:** v3-data-attrs in historical experiment IS ALSO FUNCTIONALLY EQUIVALENT TO ABS arm unless runner patches DEFAULT_INCLUDE_ATTRIBUTES.
- **Confounds:** Custom data-* stripped under DEFAULT_INCLUDE_ATTRIBUTES. Requires explicit runner patch to be observable. Historical runner used DEFAULT — token was STRIPPED.

### v4-evidence-meta (`META (excluded)`)
- **Channel:** meta tags
- **Model Sees Token:** False
- **Via DOM Snapshot:** False
- **Via Vision:** False
- **Confounds:** meta in DISABLED_ELEMENTS — token never delivered. Correctly excluded from main experiment.


---

## Phase F: Experimental Design & Randomization

### Historical Design Flaw
- Type: Sequential variant-blocked
- Fatal flaw: Sequential blocking means any quota failure creates non-ignorable differential missingness across arms.


### Proposed v3 RCBD
- Block size: 24 runs (K=4 arms × J=6 tasks)
- Planned: 96 total runs (4 blocks)
- Balance guarantee: Any complete block (24 runs) is perfectly balanced across all 4 arms x 6 tasks.
- 90 runs valid for 4-arm 6-task RCBD? **False** — 90 is NOT divisible by 24 (= 3.75 blocks). Any protocol specifying 90 runs is arithmetically inconsistent with a 4-arm 6-task RCBD.


---

## Phase G: Statistical Power

| Contrast | Delta | N=24/arm (96 total) | N=30/arm (120 total) |
|----------|-------|----------------------|----------------------|
| ABS_vs_VIS_presence_vs_absence | 0.70 | 100.0% | 100.0% |
| VIS_vs_ARIA_large_channel_degradation | 0.35 | 75.1% | 84.3% |
| VIS_vs_DATA_CFG_moderate_channel_effect | 0.20 | 35.6% | 43.0% |
| ARIA_vs_DATA_CFG_small_channel_effect | 0.15 | 23.3% | 28.2% |

---

## Phase H: Quota / Cost / Execution Safety

- Estimated requests for 96 runs: **576** (exceeds free 500/day: True)
- Hard quota guard: abort experiment after 3 consecutive 429 errors.
- Per-run timeout: 120s hard limit to prevent single run consuming disproportionate budget.
- Cache disable: CDP Network.setCacheDisabled(True) + context.clear_cookies() between runs.
- Pre-run cart state assertion: verify window.__cart__ is empty (T1-T4,T6) or contains wh-001 (T5) before agent launch.
- use_vision=False for all runs (eliminates vision confound for VIS arm).

---

## Phase I: Literature & Novelty Limitations

### Novelty Claim
Use Gemini paid tier (pay-as-you-go). 96 runs ≈ $0.30–$0.60 at current token prices. Set hard quota guard: abort after N consecutive 429s.

### Limitations
- Single agent (browser-use 0.13.10 + Gemini) — results may not generalize to other LLM/agent stacks.
- Single website (TechMart) — controlled but artificial; real-world sites have dynamic JS rendering.
- v1-jsonld arm is functionally equivalent to ABS under current browser-use serializer — does not test JSON-LD delivery.
- v3-data-attrs requires runner patch to DEFAULT_INCLUDE_ATTRIBUTES — historical runs did not include this patch.
- Vision confound if use_vision=True — VIS arm gets dual-channel (text + image) reinforcement.
- N=96 provides <80% power for small effects (delta<=0.15) — equivalence claims not supportable.
- No inter-rater reliability on verifier correctness — single automated verifier with known flaws.

### Threats to Internal Validity
- T3/T4/T5 verifier flaws mean historical success rates are contaminated and not valid for publication.
- Sequential blocking in historical experiment → MNAR truncation → no valid treatment comparisons possible from historical data.
