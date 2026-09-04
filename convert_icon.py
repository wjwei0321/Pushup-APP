import base64
from PIL import Image
import io

img_path = r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788516294533.jpg"

img = Image.open(img_path).convert("L")

from PIL import ImageOps
inverted = ImageOps.invert(img)

threshold = 128
mask = inverted.point(lambda p: 255 if p > threshold else 0)

bbox = mask.getbbox()
if bbox:
    mask = mask.crop(bbox)

# The original figure is fairly wide. Let's make it max 200.
mask.thumbnail((200, 200), Image.LANCZOS)

width, height = mask.size

buffer = io.BytesIO()
mask.save(buffer, format="PNG")
b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

svg = f"""    'Glutes Medius Slide Plank': '<svg width="100%" height="100%" viewBox="0 0 {width} {height}"><mask id="mask_Glutes_Medius_Slide_Plank"><image width="{width}" height="{height}" href="data:image/png;base64,{b64}" /></mask><rect width="{width}" height="{height}" fill="currentColor" mask="url(#mask_Glutes_Medius_Slide_Plank)" /></svg>'"""

with open("new_icon.txt", "w", encoding="utf-8") as f:
    f.write(svg)
print("Done, width=", width, "height=", height)
