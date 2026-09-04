from PIL import Image

img1 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788520200948.png")
img2 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788520200694.png")

def find_icon_rows(img):
    w, h = img.size
    pix = img.load()
    rows = []
    # scan vertically through the middle column
    for y in range(700, 1000):
        # search horizontally for non-white pixels
        has_pixel = False
        for x in range(30, w-30):
            p = pix[x, y]
            if p[0] < 250 or p[1] < 250 or p[2] < 250:
                has_pixel = True
                break
        rows.append(has_pixel)
        
    # find continuous segments of has_pixel
    segments = []
    in_segment = False
    start = 0
    for i, has_pixel in enumerate(rows):
        if has_pixel and not in_segment:
            in_segment = True
            start = i
        elif not has_pixel and in_segment:
            in_segment = False
            segments.append((start + 700, i + 700))
    return segments

print("Image 1 (Push-up):", find_icon_rows(img1))
print("Image 2 (Glutes Plank):", find_icon_rows(img2))
