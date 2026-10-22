"""TechMart Experiment 2 verifier."""

HARD_TARGETS = {
    "H1": {
        "sku": "wh-003",
        "name": "AudioMax BT50",
    },
    "H2": {
        "sku": "wh-002",
        "name": "BudPro Wireless X",
    },
    "H3": {
        "sku": "mkp-001",
        "name": "Mechanical Keyboard Pro",
    },
    "H4": {
        "sku": "wh-002",
        "name": "BudPro Wireless X",
    },
    "H5": {
        "sku": "wh-002",
        "name": "BudPro Wireless X",
    },
}


def verify_cart_state(cart, task_id):
    """Strict state-based verifier for Exp2 cart tasks."""
    target = HARD_TARGETS.get(task_id)

    if target is None:
        return {
            "success": False,
            "partial_score": 0.0,
            "details": {"error": f"Unknown Exp2 task: {task_id}"},
        }

    if not isinstance(cart, list):
        return {
            "success": False,
            "partial_score": 0.0,
            "details": {"error": "Cart state is not a list"},
        }

    matching = [
        item for item in cart
        if isinstance(item, dict) and item.get("sku") == target["sku"]
    ]

    success = len(matching) > 0

    return {
        "success": success,
        "partial_score": 1.0 if success else 0.0,
        "details": {
            "target_sku": target["sku"],
            "target_name": target["name"],
            "cart_skus": [
                item.get("sku")
                for item in cart
                if isinstance(item, dict)
            ],
            "target_present": success,
        },
    }


def verify_order_state(order_confirmed, task_id, cart):
    """Not used by current H1-H5 tasks."""
    return {
        "success": False,
        "partial_score": 0.0,
        "details": {
            "error": "Exp2 H1-H5 are cart-selection tasks; no order verifier configured.",
            "task_id": task_id,
            "order_confirmed": bool(order_confirmed),
        },
    }


def self_test():
    failures = []

    for task_id, target in HARD_TARGETS.items():
        good = verify_cart_state(
            [{"sku": target["sku"], "name": target["name"], "quantity": 1}],
            task_id,
        )
        if not good["success"]:
            failures.append(f"{task_id}: correct target failed")

        wrong_sku = "wh-001" if target["sku"] != "wh-001" else "wh-002"
        bad = verify_cart_state(
            [{"sku": wrong_sku, "name": "Wrong", "quantity": 1}],
            task_id,
        )
        if bad["success"]:
            failures.append(f"{task_id}: wrong target passed")

        empty = verify_cart_state([], task_id)
        if empty["success"]:
            failures.append(f"{task_id}: empty cart passed")

    if failures:
        raise RuntimeError("Exp2 verifier self-test failed: " + "; ".join(failures))

    print("Exp2 verifier self-test: PASS")


if __name__ == "__main__":
    self_test()
