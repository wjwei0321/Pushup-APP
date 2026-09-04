from PIL import Image

img2 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788520200694.png")

def find_orange_circle(img):
    w, h = img.size
    pix = img.load()
    for y in range(700, 1000):
        for x in range(30, 200):
            p = pix[x, y]
            if p[0] > 230 and p[1] > 140 and p[2] < 50:
                return x, y
    return -1, -1

print("Image 2 orange circle:", find_orange_circle(img2))
