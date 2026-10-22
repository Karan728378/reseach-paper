# Verifier Flaw Report
**Audit Date:** 2026-10-18
**Source:** `runner/verifier.py` (Protocol v2)

## Summary
Three verifier functions have confirmed logical flaws that contaminate all historical success-rate
measurements. These flaws affect every variant and every repetition in the main experiment.

## Flaw Details

### T3 — `verify_cart_state`
- **Flaw:** Accepted `wh-001` (lowest-rated audio item) as a valid T3 success.
  T3 requires the *second-highest* rated item (`wh-002`). The verifier checked
  `cart_contains_sku` (any inclusion) instead of `cart_exact_match` (only wh-002, length==1).
- **Impact:** Any run where the agent added wh-001 instead of wh-002 was incorrectly scored SUCCESS.
- **Evidence:** `runner/verifier.py ~L350-420`; task-definitions.json `T3.success_criterion.type = cart_exact_match`
  was added in v2 but legacy verifier.py did not enforce it.

### T4 — `verify_order_state`
- **Flaw:** `partial_score=0.25` awarded unconditionally on failure path (checkout_reached step
  scored True even when `window.__orderConfirmed__ === false`).
- **Impact:** All T4 failures show `partial_score=0.25` regardless of actual agent progress.
  Partial scores are inflated and not meaningful.
- **Evidence:** `runner/verifier.py ~L450-520`; CSV confirms all T4 failures have `partial_score=0.25`.

### T5 — `verify_cart_state` (empty-cart check)
- **Flaw:** Success criterion `window.__cart__.length === 0` passes vacuously if the
  `setup_script` (localStorage seeding) fails silently before agent launch.
  If cart was never seeded with wh-001, an agent that does nothing scores SUCCESS.
- **Impact:** T5 success rates may include vacuous passes where agent performed no meaningful action.
- **Evidence:** `tasks/task-definitions.json T5.setup_script` exists but runner does not
  assert pre-run cart state before agent launch.

## Substring Match False Positives

For retrieval tasks using numeric targets (T1: "36 months", T3: "43 units", T4: "45 days"):
- Naive substring matching on `final_result` text can trigger on agent refusal sentences.
- Example: "There is no 36 month warranty shown" → substring "36" matches → **FALSE POSITIVE SUCCESS**.
- **Fix required:** Use regex word-boundary match AND require match only in a structured
  `extracted_value` field, not free-form reasoning text.

## Recommended Fixes (do not implement until approved)

1. T3: `success = len(cart)==1 and cart[0].sku == 'wh-002'`
2. T4: `success = orderConfirmed and any(i.sku=='mse-001' for i in lastOrder.items)`; partial steps verified independently.
3. T5: Add pre-run assertion: `assert cart_contains(wh-001)` before agent launch.
4. All: Replace substring match with `re.search(r'\b36\b', final_result)` + field isolation.
