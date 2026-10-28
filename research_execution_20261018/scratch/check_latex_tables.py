import re

with open('research_paper_final.tex', 'r', encoding='utf-8') as f:
    text = f.read()

# Match tabular, tabularx, tabular*
pattern = r'\\begin\{(tabular\*?|tabularx)\}(?:\{[^}]+\})?\{([^}]+)\}(.*?)\\end\{\1\}'
matches = list(re.finditer(pattern, text, re.DOTALL))
print(f'Total tabular environments found: {len(matches)}')

for i, match in enumerate(matches, 1):
    env_type = match.group(1)
    col_spec = match.group(2)
    body = match.group(3)
    
    clean_spec = re.sub(r'@\{[^}]*\}', '', col_spec)
    clean_spec = re.sub(r'\\extracolsep\{[^}]*\}', '', clean_spec)
    
    cols = 0
    mults = re.findall(r'\*\{(\d+)\}\{([^}]+)\}', clean_spec)
    clean_spec = re.sub(r'\*\{(\d+)\}\{([^}]+)\}', '', clean_spec)
    for m_count, m_spec in mults:
        cols += int(m_count) * len(re.findall(r'[lcrXpmb]', m_spec))
    cols += len(re.findall(r'[lcrXpmb]', clean_spec))
    
    print(f'\nTable {i}: {env_type} with col_spec "{col_spec}" -> expected {cols} cols')
    
    lines = [r.strip() for r in body.split(r'\\') if r.strip()]
    for idx, r in enumerate(lines, 1):
        clean_r = re.sub(r'\\(toprule|bottomrule|midrule|hline)', '', r).strip()
        if not clean_r or clean_r.startswith('%'):
            continue
        if r'\multicolumn' in clean_r:
            print(f'  Row {idx} (multicolumn): OK')
            continue
        amps = clean_r.count('&')
        if amps != cols - 1:
            print(f'  MISMATCH Row {idx}: {amps} amps, expected {cols - 1}: {clean_r[:60]}')
        else:
            print(f'  Row {idx}: {amps} amps (OK)')
