import os, sys, glob, docx, fitz

sys.stdout.reconfigure(encoding='utf-8')

def extract_body(md_path):
    with open(md_path, encoding='utf-8') as f:
        content = f.read()
    parts = content.split('---', 2)
    if len(parts) >= 3:
        return parts[2].strip()
    return content.strip()

print("==================== BLOG 1: Aradhana ====================")
md1_path = "src/content/stories/never-ending-reincarnations-artist.md"
doc = docx.Document(r"C:\Users\bhara\Downloads\DIGITAL JOURNALISM WEBSITE-20261022T013821Z-1-001\DIGITAL JOURNALISM WEBSITE\Blog\Aradhana.docx")
orig1_paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
print("ORIGINAL PARAGRAPHS COUNT:", len(orig1_paragraphs))
for idx, p in enumerate(orig1_paragraphs):
    print(f"[{idx+1}] {p[:80]}...")

print("\nPUBLISHED BODY:")
pub1 = extract_body(md1_path)
pub1_paras = [p.strip() for p in pub1.split("\n\n") if p.strip()]
print("PUBLISHED PARAGRAPHS COUNT:", len(pub1_paras))
for idx, p in enumerate(pub1_paras):
    print(f"[{idx+1}] {p[:80]}...")

print("\n==================== BLOG 2: Dhanushree ====================")
md2_path = "src/content/stories/finding-marakkave-ninaikiren.md"
pdf2 = fitz.open(r"C:\Users\bhara\Downloads\DIGITAL JOURNALISM WEBSITE-20261022T013821Z-1-001\DIGITAL JOURNALISM WEBSITE\Blog\Dhanushree.pdf")
orig2_text = ""
for page in pdf2:
    orig2_text += page.get_text() + "\n"
orig2_paras = [p.strip() for p in orig2_text.split("\n\n") if p.strip()]
print("ORIGINAL PAGES:", len(pdf2))
print("PUBLISHED BODY:")
pub2 = extract_body(md2_path)
print("Pub2 len:", len(pub2))

print("\n==================== BLOG 3: Mithraa ====================")
md3_path = "src/content/stories/is-it-a-privilege.md"
pdf3 = fitz.open(r"C:\Users\bhara\Downloads\DIGITAL JOURNALISM WEBSITE-20261022T013821Z-1-001\DIGITAL JOURNALISM WEBSITE\Blog\Mithraa.pdf")
orig3_text = ""
for page in pdf3:
    orig3_text += page.get_text() + "\n"
print("ORIGINAL PAGES:", len(pdf3))
print("PUBLISHED BODY:")
pub3 = extract_body(md3_path)
print("Pub3 len:", len(pub3))
