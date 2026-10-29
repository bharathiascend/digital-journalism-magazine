import os, sys, fitz

sys.stdout.reconfigure(encoding='utf-8')

def extract_body(md_path):
    with open(md_path, encoding='utf-8') as f:
        content = f.read()
    parts = content.split('---', 2)
    return parts[2].strip() if len(parts) >= 3 else content.strip()

print("=== DETAILED CHECK: DHANUSHREE BLOG ===")
pdf2 = fitz.open(r"C:\Users\bhara\Downloads\DIGITAL JOURNALISM WEBSITE-20261022T013821Z-1-001\DIGITAL JOURNALISM WEBSITE\Blog\Dhanushree.pdf")
orig2_text = ""
for page in pdf2:
    orig2_text += page.get_text() + "\n"

print("--- ORIGINAL PDF TEXT ---")
print(orig2_text)
print("--- PUBLISHED MD BODY ---")
print(extract_body("src/content/stories/finding-marakkave-ninaikiren.md"))

print("\n=== DETAILED CHECK: MITHRAA BLOG ===")
pdf3 = fitz.open(r"C:\Users\bhara\Downloads\DIGITAL JOURNALISM WEBSITE-20261022T013821Z-1-001\DIGITAL JOURNALISM WEBSITE\Blog\Mithraa.pdf")
orig3_text = ""
for page in pdf3:
    orig3_text += page.get_text() + "\n"

print("--- ORIGINAL PDF TEXT ---")
print(orig3_text)
print("--- PUBLISHED MD BODY ---")
print(extract_body("src/content/stories/is-it-a-privilege.md"))
