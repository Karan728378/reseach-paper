"""
Deterministic Schedule Generator for Option A (Clean 3-Arm RCBD)
Part of: "The DOM Serialization Gap" Research Infrastructure

Arms:
1. ABS (v0-baseline)
2. ARIA (v2-aria)
3. DATA-CFG (v3-data-attrs)

Design:
Randomized Complete Block Design (RCBD)
4 temporal blocks (B1, B2, B3, B4)
6 tasks (T1, T2, T3, T4, T5, T6)
18 trials per block = 72 trials total
Zero redundant baseline replicates.
"""

import csv
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_CSV = BASE_DIR / "proposed_3arm_schedule.csv"

# Canonical task to target entity SKU mapping
TASK_ENTITY_MAP = {
    "T1": "wh-001",
    "T2": "mkp-001",
    "T3": "wh-002",
    "T4": "mse-001",
    "T5": "wh-001",
    "T6": "wh-001"
}

ARM_VARIANT_MAP = {
    "ABS": "v0-baseline",
    "ARIA": "v2-aria",
    "DATA-CFG": "v3-data-attrs"
}

def generate_3arm_schedule(seed: int = 42):
    rng = random.Random(seed)
    arms = ["ABS", "ARIA", "DATA-CFG"]
    tasks = ["T1", "T2", "T3", "T4", "T5", "T6"]
    
    rows = []
    run_index = 1
    
    for block_id in range(1, 5):
        # Generate all 18 combinations for this block
        block_combos = [(arm, task) for arm in arms for task in tasks]
        # Shuffle deterministically within block
        rng.shuffle(block_combos)
        
        for within_block_order, (arm, task) in enumerate(block_combos, 1):
            rows.append({
                "run_index": run_index,
                "block_id": block_id,
                "within_block_order": within_block_order,
                "arm": arm,
                "task_id": task,
                "variant_mapping": ARM_VARIANT_MAP[arm],
                "target_entity": TASK_ENTITY_MAP[task]
            })
            run_index += 1
            
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["run_index", "block_id", "within_block_order", "arm", "task_id", "variant_mapping", "target_entity"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Successfully generated {len(rows)} runs in {OUTPUT_CSV}")
    return rows

if __name__ == "__main__":
    generate_3arm_schedule()
