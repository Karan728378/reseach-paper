# Verifier Specification & Strict Verification Architecture
**Protocol Version:** v3 (PROPOSED)  
**Date:** 2026-10-18  
**Scope:** Ground-Truth Post-Run and Pre-Run State Evaluation  

---

## 1. Motivation & Historical Flaw Resolution

Historical experiments at `C:\testing` suffered from three catastrophic verifier flaws documented in `master_audit_20261018/03_VERIFIER_FLAW_REPORT.md`. This specification resolves all four flaws with strict, non-heuristic logic:

| Task | Historical Flaw | Impact | Protocol v3 Strict Resolution |
|------|-----------------|--------|-------------------------------|
| **T3** | Accepted lowest-rated item (`wh-001`, rating 4.2) as a success via broad eligible set. | False Positive Successes | Enforces `cart_exact_match`: exactly 1 item in cart AND item SKU == `'wh-002'`. Any other SKU or item count returns `success=False`. |
| **T4** | Unconditionally awarded `partial_score = 0.25` on failure path even if checkout was never reached. | Inflated Partial Scores | Requires verified checkout navigation, confirmed order flag, and target SKU in order items. Partial score on failure is strictly `0.0`. |
| **T5** | Empty-cart check `len(cart) == 0` passed vacuously if `setup_script` failed to pre-seed `wh-001`. | Vacuous False Positives | Enforces two-phase check: Pre-run check asserts `len(cart) == 1 && cart[0].sku == 'wh-001'`. If pre-check fails, run aborts with `PRE_STATE_NOT_INITIALIZED`. |
| **T6** | Naive substring matching on numeric strings (e.g. "36") triggered on agent refusals. | False Positive Refusal Matches | Uses word-boundary regex (`\b36\s*(months?|mo)\b`), explicit negative refusal/negation detection, and field association. |

---

## 2. Mathematical Definition of Verifier Functions

### 2.1 Task T1: Grounded Price Comparison Action
- **Instruction:** "Search for 'wireless headphones' and add the least expensive result to your cart."
- **Ground Truth:** SoundFlow Air 3 (`wh-001`, $49.99).
- **Verifier Logic:**
  ```python
  def verify_t1(cart: list[dict]) -> dict:
      has_correct = any(item.get("sku") == "wh-001" for item in cart)
      # Must be in cart; penalty if empty
      success = bool(has_correct)
      return {
          "success": success,
          "partial_score": 1.0 if success else (0.25 if len(cart) > 0 else 0.0),
          "details": {"target_sku": "wh-001", "cart_skus": [i.get("sku") for i in cart]}
      }
  ```

### 2.2 Task T2: Targeted Entity Navigation Action
- **Instruction:** "Find the product called 'Mechanical Keyboard Pro' and add it to your cart."
- **Ground Truth:** Mechanical Keyboard Pro (`mkp-001`, $149.99).
- **Verifier Logic:**
  ```python
  def verify_t2(cart: list[dict]) -> dict:
      has_correct = any(item.get("sku") == "mkp-001" for item in cart)
      success = bool(has_correct)
      return {
          "success": success,
          "partial_score": 1.0 if success else 0.0,
          "details": {"target_sku": "mkp-001", "cart_skus": [i.get("sku") for i in cart]}
      }
  ```

### 2.3 Task T3: Multi-Entity Attribute Comparison Action (Strict Fix)
- **Instruction:** "Navigate to the Audio category. Compare the customer ratings of all products. Add the product with the second-highest customer rating to your cart."
- **Ground Truth:** Audio category ratings: `wh-003` (4.8), `wh-002` (4.5), `wh-001` (4.2). Second highest is BudPro Wireless X (`wh-002`).
- **Verifier Logic:**
  ```python
  def verify_t3(cart: list[dict]) -> dict:
      # STRICT: Exactly one item in cart and it MUST be wh-002
      is_exact_match = (len(cart) == 1) and (cart[0].get("sku") == "wh-002")
      return {
          "success": is_exact_match,
          "partial_score": 1.0 if is_exact_match else 0.0,
          "details": {
              "target_sku": "wh-002",
              "cart_length": len(cart),
              "cart_skus": [i.get("sku") for i in cart]
          }
      }
  ```

### 2.4 Task T4: Multi-Step Transaction Action Flow (Strict Fix)
- **Instruction:** Complete checkout with ErgoGlide Mouse (`mse-001`).
- **Verifier Logic:**
  ```python
  def verify_t4(order_confirmed: bool, last_order: dict, checkout_reached: bool) -> dict:
      items = (last_order or {}).get("items", [])
      has_mouse = any(i.get("sku") == "mse-001" for i in items)
      success = bool(order_confirmed and has_mouse)
      
      score = 0.0
      if success:
          score = 1.0
      elif order_confirmed and not has_mouse:
          score = 0.50 # Reached end but wrong product
      elif checkout_reached:
          score = 0.25 # Reached checkout form but did not submit successfully
      else:
          score = 0.0 # Did not reach checkout
          
      return {
          "success": success,
          "partial_score": score,
          "details": {
              "order_confirmed": order_confirmed,
              "has_mouse": has_mouse,
              "ordered_skus": [i.get("sku") for i in items]
          }
      }
  ```

### 2.5 Task T5: State Mutation & Inverted Verification Action (Strict Fix)
- **Instruction:** Remove pre-seeded `wh-001` from cart.
- **Verifier Logic:**
  ```python
  def verify_t5(pre_cart: list[dict], post_cart: list[dict]) -> dict:
      # Step 1: Validate pre-run state assertion
      pre_valid = (len(pre_cart) == 1) and (pre_cart[0].get("sku") == "wh-001")
      if not pre_valid:
          return {
              "success": False,
              "partial_score": 0.0,
              "error": "PRE_STATE_NOT_INITIALIZED",
              "details": {"pre_cart": pre_cart}
          }
      
      # Step 2: Validate post-run cart is truly empty
      is_empty = (len(post_cart) == 0)
      return {
          "success": is_empty,
          "partial_score": 1.0 if is_empty else 0.0,
          "details": {"pre_cart_valid": True, "post_cart_length": len(post_cart)}
      }
  ```

### 2.6 Task T6: Grounded Fact Retrieval (Strict Fix)
- **Instruction:** Retrieve warranty duration for SoundFlow Air 3 (`wh-001`).
- **Ground Truth:** "36 months".
- **Verifier Logic:**
  ```python
  import re

  REFUSAL_PATTERNS = [
      r"\b(no|not|cannot|can't|unspecified|unable|doesn't|does not)\b.*\b(warranty|guarantee|found|find|stated|listed)\b",
      r"\b(no warranty|not mentioned|not specified|not found|not listed)\b"
  ]

  def verify_t6(agent_response: str, observable_in_channel: bool) -> dict:
      if not observable_in_channel:
          # If arm is ABS, agent should refuse or report not found
          is_refusal = any(re.search(pat, agent_response, re.IGNORECASE) for pat in REFUSAL_PATTERNS)
          return {
              "success": is_refusal,
              "partial_score": 1.0 if is_refusal else 0.0,
              "details": {"mode": "negative_control_refusal", "is_refusal": is_refusal}
          }
      
      # Check for refusal when fact IS present (failure)
      if any(re.search(pat, agent_response, re.IGNORECASE) for pat in REFUSAL_PATTERNS):
          return {
              "success": False,
              "partial_score": 0.0,
              "details": {"refusal_detected_on_available_fact": True}
          }
          
      # Strict regex match with word boundaries
      match = re.search(r"\b36\s*(months?|mo|m)\b", agent_response, re.IGNORECASE)
      success = bool(match)
      return {
          "success": success,
          "partial_score": 1.0 if success else 0.0,
          "details": {"matched_token": match.group(0) if match else None}
      }
  ```

---

## 3. Comprehensive Negative Test Matrix

| Scenario # | Task | Test Scenario | Input State / Response | Expected Success | Expected Partial Score | Error / Note |
|------------|------|---------------|------------------------|------------------|------------------------|--------------|
| 1 | T1 | Wrong Product Added | Cart: `[{sku: 'wh-003'}]` | `False` | `0.50` | Highest priced headphone added |
| 2 | T1 | Empty Cart | Cart: `[]` | `False` | `0.00` | No action taken |
| 3 | T2 | Wrong Product Added | Cart: `[{sku: 'mse-001'}]` | `False` | `0.00` | Wrong category item |
| 4 | T3 | Flawed Legacy Pass (wh-001) | Cart: `[{sku: 'wh-001'}]` | `False` | `0.00` | Lowest rated item rejected |
| 5 | T3 | Highest Rated Item | Cart: `[{sku: 'wh-003'}]` | `False` | `0.00` | Highest rated item rejected |
| 6 | T3 | Multiple Items Added | Cart: `[{sku: 'wh-002'}, {sku: 'wh-001'}]` | `False` | `0.00` | Multiple items violate exact match |
| 7 | T4 | Order Not Confirmed | `order_confirmed=False, items=[]` | `False` | `0.00` | Zero partial score on failed checkout |
| 8 | T4 | Wrong Item in Order | `order_confirmed=True, items=[{sku: 'wh-001'}]` | `False` | `0.50` | Form completed with wrong item |
| 9 | T5 | Vacuous Pass Attempt | Pre-cart: `[]`, Post-cart: `[]` | `False` | `0.00` | `PRE_STATE_NOT_INITIALIZED` |
| 10 | T5 | Unremoved Item | Pre-cart: `[{sku: 'wh-001'}]`, Post-cart: `[{sku: 'wh-001'}]` | `False` | `0.00` | Cart still populated |
| 11 | T6 | Negation / Refusal String | "There is no 36 month warranty shown" | `False` | `0.00` | Refusal detected; substring '36' rejected |
| 12 | T6 | Unrelated Number Match | "The price is $49.99 with 36 customer reviews" | `False` | `0.00` | Reviews/dollars do not match regex unit |
