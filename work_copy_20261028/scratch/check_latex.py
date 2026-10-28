import re
from pathlib import Path

tex_file = Path("research_paper_final.tex")
bib_file = Path("references.bib")

print("=== CHECKING LATEX INTEGRITY ===")
tex_text = tex_file.read_text(encoding="utf-8")
bib_text = bib_file.read_text(encoding="utf-8")

# 1. Check citations
bib_keys = set(re.findall(r"@\w+\{([^,]+),", bib_text))
print(f"Total BibTeX keys found: {len(bib_keys)}")

cited_keys = set()
for match in re.findall(r"\\cite\{([^}]+)\}", tex_text):
    for k in match.split(","):
        cited_keys.add(k.strip())
print(f"Total cited keys found: {len(cited_keys)}")

missing_citations = cited_keys - bib_keys
if missing_citations:
    print(f"ERROR: Missing citations in bib: {missing_citations}")
else:
    print("SUCCESS: All cited keys are defined in references.bib!")

# 2. Check balanced environments
env_starts = re.findall(r"\\begin\{([^}]+)\}", tex_text)
env_ends = re.findall(r"\\end\{([^}]+)\}", tex_text)
print(f"Total \\begin environments: {len(env_starts)}")
print(f"Total \\end environments: {len(env_ends)}")
if len(env_starts) == len(env_ends):
    print("SUCCESS: Balanced environment counts match!")
else:
    print(f"WARNING: Environment mismatch: {len(env_starts)} begins vs {len(env_ends)} ends")

# 3. Check for unescaped underscores outside math/commands/listings
unescaped_underscores = []
in_listing = False
lines = tex_text.splitlines()
for idx, line in enumerate(lines, 1):
    if "\\begin{lstlisting}" in line:
        in_listing = True
        continue
    if "\\end{lstlisting}" in line:
        in_listing = False
        continue
    if in_listing:
        continue
    # strip comments
    code_part = line.split("%")[0]
    # strip math blocks $...$ and \texttt{...} and \url{...} and \label{...} and \ref{...} and \cite{...}
    cleaned = re.sub(r"\$[^$]*\$", "", code_part)
    cleaned = re.sub(r"\\texttt\{[^}]*\}", "", cleaned)
    cleaned = re.sub(r"\\path\{[^}]*\}", "", cleaned)
    cleaned = re.sub(r"\\url\{[^}]*\}", "", cleaned)
    cleaned = re.sub(r"\\label\{[^}]*\}", "", cleaned)
    cleaned = re.sub(r"\\ref\{[^}]*\}", "", cleaned)
    cleaned = re.sub(r"\\cite\{[^}]*\}", "", cleaned)
    cleaned = re.sub(r"\\lstinline[|^].*?[|^]", "", cleaned)
    # look for raw _ not preceded by \
    raw_underscores = re.findall(r"(?<!\\)_", cleaned)
    if raw_underscores:
        unescaped_underscores.append((idx, line[:80]))

if unescaped_underscores:
    print(f"WARNING: Found {len(unescaped_underscores)} lines with possible unescaped underscores:")
    for l_num, text in unescaped_underscores[:5]:
        print(f"  Line {l_num}: {text}")
else:
    print("SUCCESS: Zero unescaped underscores detected!")

print("=== LATEX INTEGRITY CHECK COMPLETE ===")
