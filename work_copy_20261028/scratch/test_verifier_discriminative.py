import sys
sys.path.insert(0, "C:/testing/research_execution_20261018")
from protocol_v3_runner import verify_task_result, verify_t6_grounded_refusal

# Test T1:
# Correct: wh-001
assert verify_task_result("T1", cart=[{"sku": "wh-001"}], order_confirmed=False, last_order_items=[])["score"] == 1.0
# Wrong: wh-002 (expensive)
assert verify_task_result("T1", cart=[{"sku": "wh-002"}], order_confirmed=False, last_order_items=[])["score"] == 0.0
# Empty
assert verify_task_result("T1", cart=[], order_confirmed=False, last_order_items=[])["score"] == 0.0

# Test T2:
assert verify_task_result("T2", cart=[{"sku": "mkp-001"}], order_confirmed=False, last_order_items=[])["score"] == 1.0
assert verify_task_result("T2", cart=[{"sku": "mkp-002"}], order_confirmed=False, last_order_items=[])["score"] == 0.0
assert verify_task_result("T2", cart=[], order_confirmed=False, last_order_items=[])["score"] == 0.0

# Test T3:
assert verify_task_result("T3", cart=[{"sku": "wh-002"}], order_confirmed=False, last_order_items=[])["score"] == 1.0
assert verify_task_result("T3", cart=[{"sku": "wh-003"}], order_confirmed=False, last_order_items=[])["score"] == 0.0 # highest rating
assert verify_task_result("T3", cart=[{"sku": "wh-001"}], order_confirmed=False, last_order_items=[])["score"] == 0.0 # lowest rating
assert verify_task_result("T3", cart=[{"sku": "wh-002"}, {"sku": "wh-001"}], order_confirmed=False, last_order_items=[])["score"] == 0.0 # multiple items

# Test T4:
assert verify_task_result("T4", cart=[], order_confirmed=True, last_order_items=[{"sku": "mse-001"}])["score"] == 1.0
assert verify_task_result("T4", cart=[], order_confirmed=False, last_order_items=[{"sku": "mse-001"}])["score"] == 0.0 # not confirmed
assert verify_task_result("T4", cart=[], order_confirmed=True, last_order_items=[{"sku": "kb-001"}])["score"] == 0.0 # wrong item

# Test T5:
assert verify_task_result("T5", cart=[], order_confirmed=False, last_order_items=[], pre_cart_count=1)["score"] == 1.0
assert verify_task_result("T5", cart=[{"sku": "wh-001"}], order_confirmed=False, last_order_items=[], pre_cart_count=1)["score"] == 0.0 # not empty
assert verify_task_result("T5", cart=[], order_confirmed=False, last_order_items=[], pre_cart_count=0)["score"] == 0.0 # pre_cart was 0
assert verify_task_result("T5", cart=[], order_confirmed=False, last_order_items=[], pre_cart_count=None)["score"] == 0.0 # missing pre_cart

# Test T6:
assert verify_t6_grounded_refusal("No manufacturer warranty is listed for this item.")["score"] == 1.0
assert verify_t6_grounded_refusal("The warranty is 2 years.")["score"] == 0.0 # duration hallucination
assert verify_t6_grounded_refusal("I could not find a warranty, but it is typically 12 months.")["score"] == 0.0 # contradictory refusal + hallucination
assert verify_t6_grounded_refusal("Here is the product info.")["score"] == 0.0 # ambiguous non-refusal
assert verify_t6_grounded_refusal("")["score"] == 0.0 # empty

print("All verifier discriminative tests PASSED!")
