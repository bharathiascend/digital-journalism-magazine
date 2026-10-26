import glob, os

stories = glob.glob('website/src/content/stories/*.md')
print(f'Total existing story markdown files: {len(stories)}')
for s in sorted(stories):
    with open(s, 'r', encoding='utf-8') as f:
        text = f.read()
    title_line = [l for l in text.splitlines() if l.startswith('title:')]
    has_hero_src = ('"src": "/media/' in text) or ('src: "/media/' in text) or ('src: /media/' in text)
    t = title_line[0] if title_line else 'NO TITLE'
    print(f'{os.path.basename(s):50} | RealImg: {str(has_hero_src):5} | {t}')
