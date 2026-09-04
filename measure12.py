from PIL import Image

img1 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788520200948.png")

def find_9th_icon(img):
    w, h = img.size
    pix = img.load()
    # 9th icon is Glutes Medius Slide Plank, grey icon, in Row 2 (y around 840)
    for y in range(830, 880):
        # Scan across the width for the grey icon
        for x in range(30, 100):
            p = pix[x, y]
            if 140 < p[0] < 170 and 140 < p[1] < 170 and 140 < p[2] < 170:
                return x, y
    return -1, -1
    
print("Image 1 9th icon position:", find_9th_icon(img1))
