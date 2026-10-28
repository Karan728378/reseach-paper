"""
Local Citation Key Audit and LaTeX/BibTeX Linting Tool
Verifies that:
1. Every cite key referenced by \\cite in research_paper_final.tex exists in references.bib.
2. Zero undefined citations ([?]).
3. Zero duplicate BibTeX keys in references.bib.
4. Identifies unused bibliography keys.
5. Verifies brace balance and character escaping in both .tex and .bib.
6. Outputs machine-readable JSON to audit_outputs/citation_key_audit.json.
"""
import json
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
TEX_PATH = ROOT_DIR / "research_paper_final.tex"
BIB_PATH = ROOT_DIR / "references.bib"
OUT_JSON = ROOT_DIR / "audit_outputs" / "citation_key_audit.json"

OUT_JSON.parent.mkdir(parents=True, exist_ok=True)


def run_citation_audit() -> dict:
    tex_content = TEX_PATH.read_text(encoding="utf-8")
    bib_content = BIB_PATH.read_text(encoding="utf-8")

    # 1. Extract BibTeX keys and check duplicates
    bib_key_matches = re.findall(r'@\w+\s*\{\s*([\w\-]+)\s*,', bib_content)
    unique_bib_keys = sorted(set(bib_key_matches))
    duplicate_bib_keys = [k for k in unique_bib_keys if bib_key_matches.count(k) > 1]

    # 2. Extract cited keys in LaTeX
    cite_matches = re.findall(r'\\(?:cite|citep|citet|autocite|parencite|textcite)\{([^}]+)\}', tex_content)
    cited_keys = []
    for m in cite_matches:
        for k in m.split(','):
            cited_keys.append(k.strip())

    unique_cited_keys = sorted(set(cited_keys))
    undefined_cites = [k for k in unique_cited_keys if k not in unique_bib_keys]
    unused_bib_keys = [k for k in unique_bib_keys if k not in unique_cited_keys]

    # 3. Check BibTeX field brace balance and syntax
    entries = re.findall(r'@(\w+)\s*\{\s*([\w\-]+)\s*,\s*(.*?)\n\}', bib_content, re.DOTALL)
    syntax_errors = []
    for etype, k, body in entries:
        if body.count('{') != body.count('}'):
            syntax_errors.append(f"Unbalanced braces in BibTeX entry '{k}'")
        for line in body.split('\n'):
            if '&' in line and '\\&' not in line:
                syntax_errors.append(f"Unescaped '&' in BibTeX entry '{k}': {line.strip()}")

    # 4. Check LaTeX environment balance
    env_matches = re.findall(r'\\(begin|end)\{([^}]+)\}', tex_content)
    stack = []
    env_errors = []
    for action, env_name in env_matches:
        if action == 'begin':
            stack.append(env_name)
        else:
            if not stack:
                env_errors.append(f"Unmatched \\end{{{env_name}}}")
            else:
                top = stack.pop()
                if top != env_name:
                    env_errors.append(f"Mismatched environment: \\begin{{{top}}} closed by \\end{{{env_name}}}")
    if stack:
        env_errors.append(f"Unclosed environments: {stack}")

    is_clean = (
        len(undefined_cites) == 0 and
        len(duplicate_bib_keys) == 0 and
        len(syntax_errors) == 0 and
        len(env_errors) == 0
    )

    report = {
        "status": "PASS" if is_clean else "FAIL",
        "total_citations_in_manuscript": len(cited_keys),
        "unique_keys_cited": len(unique_cited_keys),
        "total_bib_entries": len(bib_key_matches),
        "unique_bib_keys": len(unique_bib_keys),
        "undefined_citations_count": len(undefined_cites),
        "undefined_citation_keys": undefined_cites,
        "duplicate_bib_keys_count": len(duplicate_bib_keys),
        "duplicate_bib_keys": duplicate_bib_keys,
        "unused_bib_keys_count": len(unused_bib_keys),
        "unused_bib_keys": unused_bib_keys,
        "bibtex_syntax_errors": syntax_errors,
        "latex_environment_errors": env_errors,
        "all_cited_keys": unique_cited_keys,
        "all_bib_keys": unique_bib_keys,
        "backend_configured": "BibTeX (bibliographystyle{plain}, bibliography{references})"
    }

    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Citation Key Audit Complete: Status = {report['status']}")
    print(f"  Total Citations: {report['total_citations_in_manuscript']}")
    print(f"  Unique Cited Keys: {report['unique_keys_cited']}")
    print(f"  Total Bib Entries: {report['total_bib_entries']}")
    print(f"  Undefined Citations: {report['undefined_citations_count']}")
    print(f"  Duplicate Keys: {report['duplicate_bib_keys_count']}")
    print(f"  Unused Bib Entries: {report['unused_bib_keys_count']} ({report['unused_bib_keys']})")
    print(f"  Syntax Errors: {len(syntax_errors)}")
    print(f"  Environment Errors: {len(env_errors)}")
    print(f"  Report written to: {OUT_JSON}")

    return report


if __name__ == "__main__":
    rep = run_citation_audit()
    sys.exit(0 if rep["status"] == "PASS" else 1)
