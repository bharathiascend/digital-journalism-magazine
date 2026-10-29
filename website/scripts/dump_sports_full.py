import os, sys, fitz, docx

sys.stdout.reconfigure(encoding='utf-8')

print("=== SPORTS 1: CHESS CULTURE (ARADHANA) ===")
doc = docx.Document(r"C:\Users\bhara\Downloads\DIGITAL JOURNALISM WEBSITE-20261022T013821Z-1-001\DIGITAL JOURNALISM WEBSITE\Sports\Aradhana.docx")
for idx, p in enumerate(doc.paragraphs):
    if p.text.strip():
        print(f"[{idx}] {p.text.strip()}")

print("\n=== SPORTS 2: HUNGARIAN GP (DHANUSHREE) ===")
pdf = fitz.open(r"C:\Users\bhara\Downloads\DIGITAL JOURNALISM WEBSITE-20261022T013821Z-1-001\DIGITAL JOURNALISM WEBSITE\Sports\Dhanushree.pdf")
for page in pdf:
    print(page.get_text())

print("\n=== SPORTS 3: TN SPORTS BUDGET (MITHRAA) ===")
pdf_m = fitz.open(r"C:\Users\bhara\Downloads\DIGITAL JOURNALISM WEBSITE-20261022T013821Z-1-001\DIGITAL JOURNALISM WEBSITE\Sports\Mithraa.pdf")
for page in pdf_m:
    print(page.get_text())
