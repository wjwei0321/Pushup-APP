from PIL import Image

img1 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788517336338.png")
img2 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788517336315.png")

def find_drag_handle(img):
    w, h = img.size
    pix = img.load()
    for y in range(h):
        p = pix[w//2, y]
        if p[0] < 240 and abs(p[0]-p[1]) < 10 and abs(p[1]-p[2]) < 10:
            return y
    return -1

def find_bottom_icon(img):
    w, h = img.size
    pix = img.load()
    for y in range(h-1, 0, -1):
        for x in range(w):
            p = pix[x, y]
            if p[0] > 200 and p[1] < 180 and p[2] < 50:
                return y
    return -1
    
print("Image 1 (Slant Board): drag_y=", find_drag_handle(img1), "icon_y=", find_bottom_icon(img1))
print("Image 2 (Glutes Plank): drag_y=", find_drag_handle(img2), "icon_y=", find_bottom_icon(img2))
