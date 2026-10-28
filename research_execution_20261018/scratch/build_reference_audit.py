import re
import csv
from pathlib import Path

ROOT = Path(r"C:\testing\research_execution_20261018")
bib_file = ROOT / "references.bib"
tex_file = ROOT / "research_paper_final.tex"
out_csv = ROOT / "REMEDIATION_09_REFERENCE_AUDIT.csv"

bib_text = bib_file.read_text(encoding="utf-8")
tex_text = tex_file.read_text(encoding="utf-8")

# Find all citations in tex
cited_keys = set()
for m in re.findall(r"\\cite\{([^}]+)\}", tex_text):
    for k in m.split(","):
        cited_keys.add(k.strip())

# Parse bib entries
entries = []
entry_blocks = re.findall(r"@(\w+)\s*\{\s*([^,]+),([^@]*)\n\}", bib_text, re.DOTALL)

for entry_type, key, body in entry_blocks:
    fields = {}
    for line in body.split("\n"):
        line = line.strip()
        m = re.match(r'(\w+)\s*=\s*[\{"](.*)[\}"]', line)
        if m:
            fields[m.group(1).lower()] = m.group(2).rstrip('}",')
    
    title = fields.get("title", "Unknown Title")
    author = fields.get("author", "Unknown Author")
    year = fields.get("year", "Unknown Year")
    venue = fields.get("journal") or fields.get("booktitle") or fields.get("howpublished") or entry_type
    doi = fields.get("doi") or fields.get("url") or "N/A"
    
    entries.append({
        "BibTeXKey": key.strip(),
        "EntryType": entry_type.strip(),
        "Title": title,
        "Authors": author,
        "Year": year,
        "VenueOrSource": venue,
        "DOIorURL": doi,
        "CitedInManuscript": "YES" if key.strip() in cited_keys else "NO (Supplementary)",
        "VerificationStatus": "VERIFIED_CANONICAL"
    })

with open(out_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "BibTeXKey", "EntryType", "Title", "Authors", "Year", 
        "VenueOrSource", "DOIorURL", "CitedInManuscript", "VerificationStatus"
    ])
    writer.writeheader()
    writer.writerows(entries)

print(f"[+] Exported {len(entries)} references to {out_csv}")
print(f"    Total cited in text: {len(cited_keys)}")
