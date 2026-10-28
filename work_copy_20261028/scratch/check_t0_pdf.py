import pypdf, os, glob

pdf_candidates = [
    'C:/Users/kr728/.gemini/antigravity-ide/brain/558aab4f-9d5a-44e6-8b6f-2741b12fd5d5/.user_uploaded/media_1793024172936.pdf'
]
for root, dirs, files in os.walk('C:/testing/work_copy_20261028'):
    for f in files:
        if f.endswith('.pdf'):
            pdf_candidates.append(os.path.join(root, f))

test_strings = [
    'Action-Label CoLocation Confound',
    'Action-Label Co-Location Confound',
    'Action-Label',
    '191 unit and integration tests',
    'Table III',
    'gemini-flash-lite-latest'
]

for pdf in pdf_candidates:
    if not os.path.exists(pdf):
        continue
    try:
        reader = pypdf.PdfReader(pdf)
        num_pages = len(reader.pages)
        full_text = ''
        for p in reader.pages:
            full_text += p.extract_text() or ''
        print(f'=== PDF: {os.path.relpath(pdf, "C:/testing/work_copy_20261028")} ({num_pages} pages, {len(full_text)} chars) ===')
        for s in test_strings:
            found = s.lower() in full_text.lower()
            print(f'  "{s}": {found}')
    except Exception as e:
        print(f'=== PDF: {pdf} ERROR: {e} ===')

# Now check root research_paper_final.tex
print('=== TEX: research_paper_final.tex ===')
tex_text = open('C:/testing/work_copy_20261028/research_paper_final.tex', 'r', encoding='utf-8').read()
for s in test_strings:
    found = s.lower() in tex_text.lower()
    print(f'  "{s}": {found}')
