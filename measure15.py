from PIL import Image

img1 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788520200948.png")
img2 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788520200694.png")

def find_drag_handle(img):
    w, h = img.size
    pix = img.load()
    for y in range(50, 150):
        p = pix[w//2, y]
        if p[0] < 240 and abs(p[0]-p[1]) < 10 and abs(p[1]-p[2]) < 10:
            return y
    return -1

print("Image 1 drag handle:", find_drag_handle(img1))
print("Image 2 drag handle:", find_drag_handle(img2))
