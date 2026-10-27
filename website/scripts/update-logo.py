import os
import base64

branding_dir = r'c:\Users\bhara\Downloads\DIGITAL JOURNALISM WEBSITE-20261022T013821Z-1-001\website\public\media\branding'
mark_path = os.path.join(branding_dir, 'glasnost-mark.png')
favicon_svg_path = r'c:\Users\bhara\Downloads\DIGITAL JOURNALISM WEBSITE-20261022T013821Z-1-001\website\public\favicon.svg'

with open(mark_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 190 190" width="190" height="190">
  <image href="data:image/png;base64,{b64}" x="0" y="0" width="190" height="190" />
</svg>
'''

with open(favicon_svg_path, 'w', encoding='utf-8') as f:
    f.write(svg_content)

print("Updated favicon.svg with official logo mark successfully!")
