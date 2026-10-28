"""
Computes balance tables (crosstabs by task and block across treatment arms)
for primary-eligible runs from CANONICAL_RUN_LEDGER.csv.
Saves output to results_v2/pilot_balance_tables.csv.
"""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER_PATH = ROOT / "CANONICAL_RUN_LEDGER.csv"
OUT_PATH = ROOT / "results_v2" / "pilot_balance_tables.csv"

def compute_balance():
    assert LEDGER_PATH.exists(), f"Ledger not found: {LEDGER_PATH}"
    df = pd.read_csv(LEDGER_PATH)
    
    # Filter for primary_eligible_39 == True
    # Column may be boolean or string 'True' / 'true'
    is_primary = df['primary_eligible_39'].astype(str).str.strip().str.lower().isin(['true', '1'])
    df_primary = df[is_primary].copy()
    
    print(f"Total rows in ledger: {len(df)}")
    print(f"Primary-eligible rows: {len(df_primary)}")
    assert len(df_primary) == 39, f"Expected 39 primary rows, got {len(df_primary)}"
    
    # Crosstab 1: Treatment Arm by Task ID
    xtab_task = pd.crosstab(df_primary['treatment_arm'], df_primary['task_id'], margins=True)
    print("\n--- Treatment Arm by Task ID ---")
    print(xtab_task)
    
    # Crosstab 2: Treatment Arm by Block ID
    xtab_block = pd.crosstab(df_primary['treatment_arm'], df_primary['block_id'], margins=True)
    print("\n--- Treatment Arm by Block ID ---")
    print(xtab_block)
    
    # Format for CSV export
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        f.write("# PILOT BALANCE TABLES (CANONICAL_RUN_LEDGER.csv, N=39 primary-eligible runs)\n")
        f.write("# Table 1: Treatment Arm by Task ID\n")
        xtab_task.to_csv(f)
        f.write("\n# Table 2: Treatment Arm by Block ID\n")
        xtab_block.to_csv(f)
        
    print(f"\nSaved balance tables to: {OUT_PATH}")

if __name__ == '__main__':
    compute_balance()
