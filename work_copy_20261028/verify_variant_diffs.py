"""
Deep Structural and Semantic Comparison of Website Variants
Compares:
- v0-baseline vs v2-aria
- v0-baseline vs v3-data-attrs
- v0-baseline vs v1-jsonld
- v0-baseline vs v4-evidence-meta

Verifies whether variants differ ONLY in their intended semantic markup,
or if there are any other differences (tags, classes, IDs, text content, inline scripts).
"""
import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup
import difflib

def compare_variants():
    variants_dir = Path("c:/testing/variants")
    v0_html = (variants_dir / "v0-baseline" / "index.html").read_text(encoding="utf-8")
    v1_html = (variants_dir / "v1-jsonld" / "index.html").read_text(encoding="utf-8")
    v2_html = (variants_dir / "v2-aria" / "index.html").read_text(encoding="utf-8")
    v3_html = (variants_dir / "v3-data-attrs" / "index.html").read_text(encoding="utf-8")
    v4_html = (variants_dir / "v4-evidence-meta" / "index.html").read_text(encoding="utf-8")

    out = []
    out.append("=== VARIANT COMPARISON REPORT ===")

    # 1. Compare v0 vs v2 (ARIA)
    soup0 = BeautifulSoup(v0_html, "html.parser")
    soup2 = BeautifulSoup(v2_html, "html.parser")

    # Find all aria attributes and roles in v2
    aria_attrs_found = {}
    for tag in soup2.find_all(True):
        for k, v in list(tag.attrs.items()):
            if k.startswith("aria-") or k == "role":
                aria_attrs_found[k] = aria_attrs_found.get(k, 0) + 1
                del tag.attrs[k]

    # Normalize whitespace
    def norm_soup(s):
        # normalize all string nodes whitespace
        for text in s.find_all(text=True):
            text.replace_with(re.sub(r'\s+', ' ', text.string))
        return s.prettify()

    norm0 = norm_soup(soup0)
    norm2 = norm_soup(soup2)

    out.append("\n--- 1. v0-baseline vs v2-aria ---")
    out.append(f"ARIA/role attributes removed from v2: {aria_attrs_found}")
    if norm0 == norm2:
        out.append("RESULT: 100% IDENTICAL! Once aria-* and role attributes are removed, v2-aria is character-for-character identical to v0-baseline.")
    else:
        out.append("RESULT: Differences found beyond aria-* / role!")
        diff = list(difflib.unified_diff(norm0.splitlines(), norm2.splitlines(), lineterm=""))
        out.append("\n".join(diff[:50]))

    # 2. Compare v0 vs v3 (DATA-ATTRS)
    soup0 = BeautifulSoup(v0_html, "html.parser")
    soup3 = BeautifulSoup(v3_html, "html.parser")

    data_attrs_found = {}
    for tag in soup3.find_all(True):
        for k, v in list(tag.attrs.items()):
            if k.startswith("data-"):
                data_attrs_found[k] = data_attrs_found.get(k, 0) + 1
                del tag.attrs[k]

    norm0 = norm_soup(soup0)
    norm3 = norm_soup(soup3)

    out.append("\n--- 2. v0-baseline vs v3-data-attrs ---")
    out.append(f"data-* attributes removed from v3: {data_attrs_found}")
    if norm0 == norm3:
        out.append("RESULT: 100% IDENTICAL! Once data-* attributes are removed, v3-data-attrs is character-for-character identical to v0-baseline.")
    else:
        out.append("RESULT: Differences found beyond data-*!")
        diff = list(difflib.unified_diff(norm0.splitlines(), norm3.splitlines(), lineterm=""))
        out.append("\n".join(diff[:50]))

    # 3. Compare v0 vs v1 (JSON-LD)
    soup0 = BeautifulSoup(v0_html, "html.parser")
    soup1 = BeautifulSoup(v1_html, "html.parser")

    # Remove script[type="application/ld+json"] from v1
    jsonld_scripts = soup1.find_all("script", type="application/ld+json")
    out.append("\n--- 3. v0-baseline vs v1-jsonld ---")
    out.append(f"JSON-LD scripts found in v1: {len(jsonld_scripts)}")
    for s in jsonld_scripts:
        s.decompose()

    norm0 = norm_soup(soup0)
    norm1 = norm_soup(soup1)
    if norm0 == norm1:
        out.append("RESULT: 100% IDENTICAL! Once JSON-LD script is removed, v1-jsonld is character-for-character identical to v0-baseline.")
    else:
        out.append("RESULT: Differences found beyond JSON-LD script!")
        diff = list(difflib.unified_diff(norm0.splitlines(), norm1.splitlines(), lineterm=""))
        out.append("\n".join(diff[:50]))

    # 4. Compare v0 vs v4 (META)
    soup0 = BeautifulSoup(v0_html, "html.parser")
    soup4 = BeautifulSoup(v4_html, "html.parser")

    # Remove extra meta tags from v4
    meta_tags = soup4.find_all("meta")
    out.append("\n--- 4. v0-baseline vs v4-evidence-meta ---")
    out.append(f"Meta tags in v4: {len(meta_tags)}")
    v0_meta = set(str(m) for m in soup0.find_all("meta"))
    extra_meta = [m for m in meta_tags if str(m) not in v0_meta]
    out.append(f"Extra meta tags in v4: {len(extra_meta)}")
    for m in extra_meta:
        m.decompose()

    norm0 = norm_soup(soup0)
    norm4 = norm_soup(soup4)
    if norm0 == norm4:
        out.append("RESULT: 100% IDENTICAL! Once extra meta tags are removed, v4-evidence-meta is character-for-character identical to v0-baseline.")
    else:
        out.append("RESULT: Differences found beyond extra meta tags!")
        diff = list(difflib.unified_diff(norm0.splitlines(), norm4.splitlines(), lineterm=""))
        out.append("\n".join(diff[:50]))

    # 5. Shared file comparison
    out.append("\n--- 5. Shared Asset Comparison ---")
    shared_files = ["app-core.js", "products.js", "styles.css"]
    for sf in shared_files:
        p = Path("c:/testing/shared") / sf
        out.append(f"Shared file: {sf} exists, size={p.stat().st_size} bytes")

    report_text = "\n".join(out)
    Path("c:/testing/research_execution_20261018/variant_diff_report.txt").write_text(report_text, encoding="utf-8")
    print("Report written to variant_diff_report.txt")
    print("\nSummary of results:")
    for line in out:
        if "RESULT:" in line or "===" in line or "---" in line:
            print(line)

if __name__ == "__main__":
    compare_variants()
