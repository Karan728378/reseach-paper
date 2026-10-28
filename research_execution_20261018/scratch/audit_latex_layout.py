import re

with open('research_paper_final.tex', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total lines: {len(lines)}')

# 1. Check all \texttt strings for length > 30 chars
long_texttt = []
for idx, line in enumerate(lines, 1):
    matches = re.findall(r'\\texttt\{([^}]+)\}', line)
    for m in matches:
        if len(m) > 25:
            long_texttt.append((idx, m))

print(f'\nFound {len(long_texttt)} long \\texttt strings (>25 chars):')
for idx, s in long_texttt:
    print(f'  Line {idx}: {s}')

# 2. Check table environments and widths
tables = re.findall(r'\\begin\{(table\*?)\}(.*?)\\end\{\1\}', ''.join(lines), re.DOTALL)
print(f'\nTotal table floats: {len(tables)}')
for idx, (ttype, tbody) in enumerate(tables, 1):
    # Check if caption exists
    cap = re.search(r'\\caption\{([^}]+)\}', tbody)
    cap_text = cap.group(1)[:40] if cap else 'NO CAPTION'
    # Check inner tabular
    tab_type = re.search(r'\\begin\{(tabular\*?|tabularx)\}(?:\{([^}]+)\})?', tbody)
    inner = tab_type.group(1) if tab_type else 'UNKNOWN'
    inner_w = tab_type.group(2) if (tab_type and tab_type.group(2)) else 'N/A'
    print(f'  Table Float {idx}: {ttype} containing {inner} (width: {inner_w}) - Caption: "{cap_text}..."')

# 3. Check equation line widths
equations = re.findall(r'\\begin\{equation\}(.*?)\\end\{equation\}', ''.join(lines), re.DOTALL)
print(f'\nTotal equation environments: {len(equations)}')
for idx, eq in enumerate(equations, 1):
    print(f'  Eq {idx}: {eq.strip()}')
