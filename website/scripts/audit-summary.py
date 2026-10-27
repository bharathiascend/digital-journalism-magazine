import glob, re

stories = []
for f in sorted(glob.glob('website/src/content/stories/*.md')):
    txt = open(f, encoding='utf-8').read().split('---')[1]
    title = re.search(r'title:\s*["\']?(.*?)["\']?\s*\n', txt)
    slug = re.search(r'slug:\s*["\']?(.*?)["\']?\s*\n', txt)
    sec = re.search(r'section:\s*["\']?(.*?)["\']?\s*\n', txt)
    fmt = re.search(r'format:\s*["\']?(.*?)["\']?\s*\n', txt)
    auth = re.search(r'name:\s*["\']?(.*?)["\']?\s*\n', txt)
    stories.append({
        'title': title.group(1) if title else '',
        'slug': slug.group(1) if slug else '',
        'section': sec.group(1) if sec else '',
        'format': fmt.group(1) if fmt else '',
        'author': auth.group(1) if auth else '',
    })

print(f"Total stories: {len(stories)}")
print("-" * 90)
for s in stories:
    slug = s.get('slug', '')
    sec = s.get('section', '')
    fmt = s.get('format', '')
    title = s.get('title', '')[:35]
    author = s.get('author', '')
    print(f"{slug:<42} | sec:{sec:<10} | fmt:{fmt:<13} | auth:{author:<10} | {title}")
