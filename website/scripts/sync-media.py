import os, shutil

SRC = 'DIGITAL JOURNALISM WEBSITE'
DEST_PHOTOS = 'website/public/media/photos'
DEST_ADS = 'website/public/media/ads'
DEST_BANNERS = 'website/public/media/banners'

os.makedirs(DEST_PHOTOS, exist_ok=True)
os.makedirs(DEST_ADS, exist_ok=True)
os.makedirs(DEST_BANNERS, exist_ok=True)

MAPPINGS = [
    # Ads
    (os.path.join(SRC, 'Advertisement', 'Aradhana_.png'), os.path.join(DEST_ADS, 'ad-borcelle-cafe.png')),
    (os.path.join(SRC, 'Advertisement', 'Dhanushree.jpg'), os.path.join(DEST_ADS, 'ad-vetri-ca.jpg')),
    (os.path.join(SRC, 'Advertisement', 'Mithraa.jpg'), os.path.join(DEST_ADS, 'ad-rhythm-media.jpg')),

    # Banners
    (os.path.join(SRC, 'Banner', 'Aradhana.png'), os.path.join(DEST_BANNERS, 'banner-fomo-klub.png')),
    (os.path.join(SRC, 'Banner', 'Dhanushree.jpg'), os.path.join(DEST_BANNERS, 'banner-serene-halloween.jpg')),

    # Blog
    (os.path.join(SRC, 'Blog', 'dhanushree.jpg'), os.path.join(DEST_PHOTOS, 'blog-dhanushree-marakkave.jpg')),
    (os.path.join(SRC, 'Blog', 'Mithraa blog image.jpeg'), os.path.join(DEST_PHOTOS, 'blog-mithraa-privilege.jpeg')),

    # Lifestyle
    (os.path.join(SRC, 'Lifestyle-Entertainment', 'Aradhana Lifestyle.jpg'), os.path.join(DEST_PHOTOS, 'lifestyle-aradhana-dalit-vegan.jpg')),
    (os.path.join(SRC, 'Lifestyle-Entertainment', 'dhanushree.jpg'), os.path.join(DEST_PHOTOS, 'lifestyle-dhanushree-natchathiram.jpg')),
    (os.path.join(SRC, 'Lifestyle-Entertainment', 'mithraa.jpeg'), os.path.join(DEST_PHOTOS, 'lifestyle-mithraa-male-loneliness.jpeg')),

    # National
    (os.path.join(SRC, 'National Story', 'Aradhana National story .jpg'), os.path.join(DEST_PHOTOS, 'national-aradhana-el-nino.jpg')),
    (os.path.join(SRC, 'National Story', 'dhanushree.jpg'), os.path.join(DEST_PHOTOS, 'national-dhanushree-sonam-wangchuk-1.jpg')),
    (os.path.join(SRC, 'National Story', 'dhanushree(1).jpg'), os.path.join(DEST_PHOTOS, 'national-dhanushree-sonam-wangchuk-2.jpg')),
    (os.path.join(SRC, 'National Story', 'mithraanatstory.jpg'), os.path.join(DEST_PHOTOS, 'national-mithraa-old-guard.jpg')),

    # News Analysis
    (os.path.join(SRC, 'News Analysis', 'Aradhana News analysis.jpg'), os.path.join(DEST_PHOTOS, 'analysis-aradhana-neet-protest.jpg')),
    (os.path.join(SRC, 'News Analysis', 'dhanushree.jpg'), os.path.join(DEST_PHOTOS, 'analysis-dhanushree-fact-check-unit.jpg')),
    (os.path.join(SRC, 'News Analysis', 'mithraa.jpeg'), os.path.join(DEST_PHOTOS, 'analysis-mithraa-custodial-deaths.jpeg')),

    # Opinion Poll
    (os.path.join(SRC, 'Opinion Poll', 'Aradhana Opinion Poll.jpg'), os.path.join(DEST_PHOTOS, 'poll-aradhana-career-choice.jpg')),
    (os.path.join(SRC, 'Opinion Poll', 'dhanushree.jpg'), os.path.join(DEST_PHOTOS, 'poll-dhanushree-dorothy-cinema.jpg')),
    (os.path.join(SRC, 'Opinion Poll', 'mithraa.jpeg'), os.path.join(DEST_PHOTOS, 'poll-mithraa-exit-polls.jpeg')),

    # Political
    (os.path.join(SRC, 'Political Story', 'Aradhana Political story image.jpg'), os.path.join(DEST_PHOTOS, 'political-aradhana-mamdani.jpg')),
    (os.path.join(SRC, 'Political Story', 'dhanushree political story.jpeg'), os.path.join(DEST_PHOTOS, 'political-dhanushree-neet-protest.jpeg')),
    (os.path.join(SRC, 'Political Story', 'dhanushree political story anitha.jpeg'), os.path.join(DEST_PHOTOS, 'political-dhanushree-anitha-memorial.jpeg')),
    (os.path.join(SRC, 'Political Story', 'mithraa pol story.jpeg'), os.path.join(DEST_PHOTOS, 'political-mithraa-genz-dmk.jpeg')),

    # Sports
    (os.path.join(SRC, 'Sports', 'Aradhana Sports story image.jpeg'), os.path.join(DEST_PHOTOS, 'sports-aradhana-chess.jpeg')),
    (os.path.join(SRC, 'Sports', 'dhanushree.jpg'), os.path.join(DEST_PHOTOS, 'sports-dhanushree-hungarian-gp.jpg')),
    (os.path.join(SRC, 'Sports', 'mithraa.jpeg'), os.path.join(DEST_PHOTOS, 'sports-mithraa-budget-jump.jpeg')),
]

for src_file, dest_file in MAPPINGS:
    if os.path.exists(src_file):
        shutil.copy2(src_file, dest_file)
        print(f"Copied: {src_file} -> {dest_file}")
    else:
        print(f"WARNING: Missing source {src_file}")

print("Media sync complete!")
