import os, re, json
import docx, pypdf

BASE_DIR = '../DIGITAL JOURNALISM WEBSITE' if os.path.exists('../DIGITAL JOURNALISM WEBSITE') else 'DIGITAL JOURNALISM WEBSITE'
OUTPUT_FILE = 'scripts/extracted_content.json' if os.path.exists('scripts') else 'website/scripts/extracted_content.json'

def read_docx(path):
    doc = docx.Document(path)
    paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return '\n\n'.join(paras)

def clean_pdf_text(raw_text):
    if not raw_text:
        return ""
    # Fix broken encodings to clean quotes and typographic symbols
    text = raw_text.replace('\ufffd', "'").replace('â€™', "'").replace('â€œ', '"').replace('â€ ', '"')
    text = text.replace('\u2018', "'").replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
    
    # Check if text uses the Canva / PDF single-word newline layout pattern (\n \n between words, \n \n \n+ between paragraphs)
    if '\n \n' in text:
        step1 = re.sub(r'(?:\n\s*){3,}', '___PARABREAK___', text)
        step2 = re.sub(r'\s*\n\s*', ' ', step1)
        restored = step2.replace('___PARABREAK___', '\n\n')
        return re.sub(r' +', ' ', restored).strip()
    else:
        # Standard PDF newline flow
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        return '\n\n'.join(lines)

def read_pdf(path):
    reader = pypdf.PdfReader(path)
    pages_text = []
    for i, page in enumerate(reader.pages):
        t = page.extract_text()
        if t:
            pages_text.append(clean_pdf_text(t))
    return '\n\n'.join(pages_text)

def main():
    catalog = {}
    for cat in sorted(os.listdir(BASE_DIR)):
        cat_path = os.path.join(BASE_DIR, cat)
        if not os.path.isdir(cat_path):
            continue
        catalog[cat] = {'docs': {}, 'media': []}
        for f in sorted(os.listdir(cat_path)):
            p = os.path.join(cat_path, f)
            ext = os.path.splitext(f)[1].lower()
            if ext == '.docx':
                text = read_docx(p)
                catalog[cat]['docs'][f] = text
            elif ext == '.pdf' and cat not in ['Banner']:
                text = read_pdf(p)
                catalog[cat]['docs'][f] = text
            else:
                catalog[cat]['media'].append(f)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        json.dump(catalog, out, indent=2, ensure_ascii=False)
    
    print(f'Successfully extracted and cataloged all content to {OUTPUT_FILE}')
    for cat, data in catalog.items():
        print(f"\n[{cat}]")
        print(f"  Docs ({len(data['docs'])}): {list(data['docs'].keys())}")
        print(f"  Media ({len(data['media'])}): {data['media']}")

if __name__ == '__main__':
    main()
