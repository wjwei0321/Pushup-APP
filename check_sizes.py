import re
import base64
import io
from PIL import Image

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Extract all EXERCISES
pattern = r"'(.*?)':\s*'<svg.*?viewBox=\"0 0 (\d+) (\d+)\".*?base64,(.*?)\".*?</svg>'"
matches = re.findall(pattern, js)

for name, vw, vh, b64 in matches:
    img_data = base64.b64decode(b64)
    img = Image.open(io.BytesIO(img_data)).convert('RGBA')
    
    # find bbox
    data = img.getdata()
    w, h = img.size
    min_x = w; max_x = 0
    min_y = h; max_y = 0
    
    for y in range(h):
        for x in range(w):
            if data[y*w+x][3] > 50:
                if x < min_x: min_x = x
                if x > max_x: max_x = x
                if y < min_y: min_y = y
                if y > max_y: max_y = y
                
    bbox_w = max_x - min_x
    bbox_h = max_y - min_y
    
    scale_y = bbox_h / int(vh)
    
    print(f"{name}: viewBox={vw}x{vh}, bbox={bbox_w}x{bbox_h}, scale_y={scale_y:.2f}")

