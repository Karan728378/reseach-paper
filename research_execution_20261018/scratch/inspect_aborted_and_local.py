import csv

print("=== V3 3ARM ABORTED ROWS ===")
with open('results/v3_3arm_summary.csv', 'r', encoding='utf-8') as f:
    reader = list(csv.DictReader(f))
for idx, r in enumerate(reader):
    if r.get('status') != 'completed':
        print(f"Row {idx+1}: run_index={r.get('run_index')}, block={r.get('block_id')}, arm={r.get('arm')}, status={r.get('status')}, error={r.get('error_message')}")

print("\n=== LOCAL LLAMA 5 ROWS ===")
with open('results/local_llama_summary.csv', 'r', encoding='utf-8') as f:
    reader = list(csv.DictReader(f))
for idx, r in enumerate(reader):
    print(f"Row {idx+1}: run_id={r.get('run_id')}, model={r.get('model')}, duration={r.get('duration_seconds')}, status={r.get('status')}, reason={r.get('termination_reason')}, error={r.get('error_message')}")
