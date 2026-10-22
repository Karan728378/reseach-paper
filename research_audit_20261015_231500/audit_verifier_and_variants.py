import os
import re
import json

verifier_path = r"C:\testing\runner\verifier.py"
runner_path = r"C:\testing\runner\agent-runner.py"
variants_dir = r"C:\testing\variants"
shared_dir = r"C:\testing\shared"

print("=== AUDITING VERIFIER.PY ===")
with open(verifier_path, "r", encoding="utf-8") as f:
    verifier_code = f.read()

# Check T3 rating check
print("\n--- T3 Verification Code Snippet ---")
t3_match = re.search(r"def verify_t3.*?(?=\ndef verify_|\Z)", verifier_code, re.DOTALL)
if t3_match:
    print(t3_match.group(0)[:1500])
else:
    # search for t3
    lines = [line for line in verifier_code.splitlines() if "t3" in line.lower() or "rating" in line.lower() or "wh-002" in line]
    print("\n".join(lines[:20]))

# Check T4 order check & __lastOrder__
print("\n--- T4 Verification Code Snippet ---")
t4_match = re.search(r"def verify_t4.*?(?=\ndef verify_|\Z)", verifier_code, re.DOTALL)
if t4_match:
    print(t4_match.group(0)[:1500])
else:
    lines = [line for line in verifier_code.splitlines() if "t4" in line.lower() or "lastorder" in line.lower() or "mse-001" in line]
    print("\n".join(lines[:20]))

# Check T5 empty cart check
print("\n--- T5 Verification Code Snippet ---")
t5_match = re.search(r"def verify_t5.*?(?=\ndef verify_|\Z)", verifier_code, re.DOTALL)
if t5_match:
    print(t5_match.group(0)[:1500])
else:
    lines = [line for line in verifier_code.splitlines() if "t5" in line.lower() or "empty" in line.lower()]
    print("\n".join(lines[:20]))

# Check SKU matching (substring vs exact)
print("\n--- Substring vs Exact SKU checks in verifier ---")
for i, line in enumerate(verifier_code.splitlines(), 1):
    if "sku" in line.lower() and ("in" in line or "==" in line or "find" in line):
        print(f"Line {i}: {line.strip()}")

print("\n=== AUDITING PRODUCTS AND RATINGS (T3 DETERMINISM) ===")
prod_path = os.path.join(shared_dir, "products.js")
if os.path.exists(prod_path):
    with open(prod_path, "r", encoding="utf-8") as f:
        prod_code = f.read()
    print("Found products.js:")
    # extract product objects
    for line in prod_code.splitlines():
        if "category" in line or "rating" in line or "sku" in line or "price" in line:
            print("  ", line.strip())

print("\n=== AUDITING APP-CORE.JS AND CART STATE ===")
app_path = os.path.join(shared_dir, "app-core.js")
if os.path.exists(app_path):
    with open(app_path, "r", encoding="utf-8") as f:
        app_code = f.read()
    for line in app_code.splitlines():
        if "__lastOrder__" in line or "__orderConfirmed__" in line or "localStorage" in line:
            print("  ", line.strip())
