import os
import browser_use
from pathlib import Path

bu_root = Path(browser_use.__file__).resolve().parent
serializer_py = bu_root / "dom" / "serializer" / "serializer.py"
views_py = bu_root / "dom" / "views.py"

print(f"Auditing serializer.py: {serializer_py}")
print(f"Auditing views.py: {views_py}")

out_lines = [
    "================================================================================",
    "BROWSER-USE 0.13.10 SOURCE LINE EVIDENCE",
    "================================================================================",
    f"Package directory: {bu_root}",
    f"serializer.py: {serializer_py}",
    f"views.py     : {views_py}",
    "--------------------------------------------------------------------------------",
]

# 1. Search DISABLED_ELEMENTS in serializer.py
ser_lines = serializer_py.read_text(encoding='utf-8').splitlines()
out_lines.append("--- 1. DISABLED_ELEMENTS in serializer.py ---")
for idx, l in enumerate(ser_lines):
    if "DISABLED_ELEMENTS" in l:
        out_lines.append(f"Line {idx+1}: {l}")
        # print next 5 lines
        for j in range(1, 6):
            if idx + j < len(ser_lines):
                out_lines.append(f"Line {idx+1+j}: {ser_lines[idx+j]}")
        break

# 2. Search where DISABLED_ELEMENTS is used in serializer.py
out_lines.append("\n--- 2. DISABLED_ELEMENTS usage in serializer.py ---")
for idx, l in enumerate(ser_lines):
    if "node.tag_name in DISABLED_ELEMENTS" in l or "in DISABLED_ELEMENTS" in l:
        for j in range(max(0, idx - 2), min(len(ser_lines), idx + 5)):
            out_lines.append(f"Line {j+1}: {ser_lines[j]}")
        break

# 3. Search non-interactive aria-label / container gate in serializer.py
out_lines.append("\n--- 3. Serializer container / aria-label / text representation gate in serializer.py ---")
for idx, l in enumerate(ser_lines):
    if "aria-label" in l or "llm_representation" in l or "get_element_text" in l or "original_node.tag_name" in l:
        if "IFRAME" in l or "aria-label" in l or "highlight_index" in l:
            out_lines.append(f"Line {idx+1}: {l}")

# Look specifically for lines around 1040-1060 in serializer.py
out_lines.append("\n--- 4. Lines 1035 to 1060 in serializer.py ---")
for idx in range(1035, min(len(ser_lines), 1060)):
    out_lines.append(f"Line {idx+1}: {ser_lines[idx]}")

# 4. Search DEFAULT_INCLUDE_ATTRIBUTES in views.py
view_lines = views_py.read_text(encoding='utf-8').splitlines()
out_lines.append("\n--- 5. DEFAULT_INCLUDE_ATTRIBUTES in views.py ---")
for idx, l in enumerate(view_lines):
    if "DEFAULT_INCLUDE_ATTRIBUTES" in l:
        out_lines.append(f"Line {idx+1}: {l}")
        for j in range(1, 15):
            if idx + j < len(view_lines):
                out_lines.append(f"Line {idx+1+j}: {view_lines[idx+j]}")
                if "]" in view_lines[idx+j]:
                    break
        break

report_text = "\n".join(out_lines)
print(report_text)

# Save to results_v2/source_line_evidence.txt
root_dir = Path(__file__).resolve().parent.parent
res_dir = root_dir / "results_v2"
res_dir.mkdir(parents=True, exist_ok=True)
out_file = res_dir / "source_line_evidence.txt"
out_file.write_text(report_text, encoding='utf-8')
print(f"\nSaved source line evidence to: {out_file}")
