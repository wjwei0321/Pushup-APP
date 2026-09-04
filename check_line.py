from PIL import Image, ImageOps

img = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788516294533.jpg").convert("L")
inverted = ImageOps.invert(img)
mask = inverted.point(lambda p: 255 if p > 128 else 0)
bbox = mask.getbbox()
print("Bounding box:", bbox)

# let's find if there's a horizontal line near the bottom of bbox
w, h = mask.size
pix = mask.load()
bottom = bbox[3] - 1

# count white pixels on the bottom 10 rows
for y in range(bottom - 10, bottom + 1):
    count = sum(1 for x in range(bbox[0], bbox[2]) if pix[x, y] == 255)
    print(f"Row {y} white pixels: {count} out of {bbox[2]-bbox[0]}")
