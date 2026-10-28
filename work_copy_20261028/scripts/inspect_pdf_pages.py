import pypdf
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

pdf_path = r"C:\Users\kr728\.gemini\antigravity-ide\brain\558aab4f-9d5a-44e6-8b6f-2741b12fd5d5\.user_uploaded\media_1793024172936.pdf"

reader = pypdf.PdfReader(pdf_path)
print(f"Total Pages: {len(reader.pages)}")

for i, page in enumerate(reader.pages):
    text = page.extract_text() or ""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    header = " | ".join(lines[:5])
    print(f"\n--- Page {i+1} ({len(lines)} lines) ---")
    print("Header:", header[:150])
    # Find section headings
    for line in lines:
        if any(h in line for h in ["ABSTRACT", "I. INTRODUCTION", "II. BACKGROUND", "III. RESEARCH", "IV. DETERMINISTIC", "V. ACCESSIBILITY", "VI. EXPERIMENTAL", "VII. STATISTICAL", "VIII. RESULTS", "IX. DISCUSSION", "X. CONCLUSION", "APPENDIX", "TABLE I", "TABLE II", "TABLE III", "TABLE IV", "TABLE V", "REFERENCES"]):
            print(f"   [Heading/Table]: {line[:90]}")
