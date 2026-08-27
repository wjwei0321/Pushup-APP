import base64
import io
import re
from PIL import Image

boxes = {
    'Push-up': (0, 0, 240, 280),
    'Pull-up': (240, 0, 450, 280),
    'Lunge': (450, 0, 670, 280),
    'Glute Band': (670, 0, 880, 280),
    'Hack Squat': (240, 388, 450, 555),
    'Romanian Deadlift': (450, 336, 670, 555),
    'Slant Board Squat': (670, 368, 880, 555)
}

img = Image.open('icons_grid.png').convert('RGBA')
svgs = {}

for name, box in boxes.items():
    cell = img.crop(box)
    data = cell.getdata()
    w, h = cell.size
    min_y = h; max_y = 0
    
    newData = []
    for y in range(h):
        for x in range(w):
            r, g, b, a = data[y * w + x]
            if a > 50:
                newData.append((255, 255, 255, a))
                if y < min_y: min_y = y
                if y > max_y: max_y = y
            else:
                newData.append((0, 0, 0, 0))
                
    cell.putdata(newData)
    
    pad = 5
    crop_box = (
        0,
        max(0, min_y - pad),
        w,
        min(h, max_y + pad)
    )
    final_img = cell.crop(crop_box)
        
    buffer = io.BytesIO()
    final_img.save(buffer, format='PNG')
    b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    fw, fh = final_img.size
    svg = f'<svg width="100%" height="100%" viewBox="0 0 {fw} {fh}"><mask id="mask_{name.replace(" ", "_")}"><image width="{fw}" height="{fh}" href="data:image/png;base64,{b64}" /></mask><rect width="{fw}" height="{fh}" fill="currentColor" mask="url(#mask_{name.replace(" ", "_")})" /></svg>'
    svgs[name] = svg

with open('app.js', 'r', encoding='utf-8') as f:
    content = f.read()

for name, svg in svgs.items():
    pattern = r"'" + re.escape(name) + r"':\s*'<svg.*?</svg>'"
    replacement = f"'{name}': '{svg}'"
    content = re.sub(pattern, replacement, content)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated all SVGs for horizontal centering.")
