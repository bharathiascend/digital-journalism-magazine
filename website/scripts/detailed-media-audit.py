import os, glob

SRC_BASE = 'DIGITAL JOURNALISM WEBSITE'

# Find all files in source
all_source_files = {}
for root, dirs, files in os.walk(SRC_BASE):
    rel_dir = os.path.relpath(root, SRC_BASE)
    for f in files:
        p = os.path.join(root, f)
        all_source_files[os.path.join(rel_dir, f).replace('\\', '/')] = os.path.getsize(p)

print(f"Total files in source directory: {len(all_source_files)}")

categories = [
    'Advertisement',
    'Banner',
    'Blog',
    'Lifestyle-Entertainment',
    'National Story',
    'News Analysis',
    'News Explainer',
    'Opinion Poll',
    'Photo Feature',
    'Podcast',
    'Political Story',
    'Sports'
]

print("\n========================================================")
print("     COMPLETE SOURCE ASSET AUDIT BY CATEGORY")
print("========================================================")

for cat in categories:
    cat_files = [k for k in all_source_files.keys() if k.startswith(cat + '/')]
    docs = [f for f in cat_files if f.endswith(('.docx', '.pdf')) and cat != 'Banner']
    images = [f for f in cat_files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    videos = [f for f in cat_files if f.lower().endswith('.mp4')]
    audios = [f for f in cat_files if f.lower().endswith(('.mp3', '.mpeg'))]
    
    print(f"\n[{cat.upper()}] - {len(cat_files)} files total")
    print(f"  Documents ({len(docs)}): {[os.path.basename(d) for d in docs]}")
    print(f"  Images ({len(images)}): {[os.path.basename(i) for i in images]}")
    if videos:
        print(f"  Videos ({len(videos)}): {[os.path.basename(v) for v in videos]}")
    if audios:
        print(f"  Audio ({len(audios)}): {[os.path.basename(a) for a in audios]}")
