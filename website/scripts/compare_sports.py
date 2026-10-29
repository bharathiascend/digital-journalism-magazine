import os, sys, fitz, docx

sys.stdout.reconfigure(encoding='utf-8')

def extract_body(md_path):
    with open(md_path, encoding='utf-8') as f:
        content = f.read()
    parts = content.split('---', 2)
    return parts[2].strip() if len(parts) >= 3 else content.strip()

print("==================== SPORTS: ARADHANA (Chess) ====================")
doc_a = docx.Document(r"C:\Users\bhara\Downloads\DIGITAL JOURNALISM WEBSITE-20261022T013821Z-1-001\DIGITAL JOURNALISM WEBSITE\Sports\Aradhana.docx")
print("DOCX Paras:", len(doc_a.paragraphs))
for i, p in enumerate(doc_a.paragraphs):
    if p.text.strip():
        print(f"P{i+1}: {p.text.strip()[:60]}")
print("--- Published Chess Body ---")
pub_chess = extract_body("src/content/stories/how-chennais-chess-culture-is-growing.md")
print(pub_chess[:300])

print("\n==================== SPORTS: DHANUSHREE (Hungarian GP) ====================")
pdf_d = fitz.open(r"C:\Users\bhara\Downloads\DIGITAL JOURNALISM WEBSITE-20261022T013821Z-1-001\DIGITAL JOURNALISM WEBSITE\Sports\Dhanushree.pdf")
d_text = ""
for page in pdf_d:
    d_text += page.get_text() + "\n"
print("PDF Pages:", len(pdf_d), "Text length:", len(d_text))
print("--- Published Hungarian GP Body ---")
pub_gp = extract_body("src/content/stories/hungarian-grand-prix-race-report.md")
print("GP Pub len:", len(pub_gp))
print(pub_gp[:300])

print("\n==================== SPORTS: MITHRAA (TN Sports Budget) ====================")
pdf_m = fitz.open(r"C:\Users\bhara\Downloads\DIGITAL JOURNALISM WEBSITE-20261022T013821Z-1-001\DIGITAL JOURNALISM WEBSITE\Sports\Mithraa.pdf")
m_text = ""
for page in pdf_m:
    m_text += page.get_text() + "\n"
print("PDF Pages:", len(pdf_m), "Text length:", len(m_text))
print("--- Published TN Sports Budget Body ---")
pub_tn = extract_body("src/content/stories/tamil-nadu-sports-budget-jump.md")
print("TN Pub len:", len(pub_tn))
print(pub_tn[:300])
