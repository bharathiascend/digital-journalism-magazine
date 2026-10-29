import os, sys, glob, docx, fitz

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\bhara\Downloads\DIGITAL JOURNALISM WEBSITE-20261022T013821Z-1-001\DIGITAL JOURNALISM WEBSITE\Sports"

print("=== SPORTS / ARADHANA ===")
doc = docx.Document(os.path.join(base_dir, "Aradhana.docx"))
for idx, p in enumerate([p.text for p in doc.paragraphs if p.text.strip()]):
    print(f"[{idx+1}] {p[:100]}...")

print("\n=== SPORTS / DHANUSHREE ===")
pdf = fitz.open(os.path.join(base_dir, "Dhanushree.pdf"))
for idx, page in enumerate(pdf):
    print(f"--- Page {idx+1} ---")
    print(page.get_text()[:400])

print("\n=== SPORTS / MITHRAA ===")
pdf_m = fitz.open(os.path.join(base_dir, "Mithraa.pdf"))
for idx, page in enumerate(pdf_m):
    print(f"--- Page {idx+1} ---")
    print(page.get_text()[:400])
