from PIL import Image

img1 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788520200948.png")
img2 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788520200694.png")

def find_orange_circle_y(img):
    w, h = img.size
    pix = img.load()
    for y in range(700, 950):
        for x in range(30, 100):
            p = pix[x, y]
            if p[0] > 230 and p[1] > 140 and p[2] < 50:
                return y
    return -1

print("Image 1 orange circle top y=", find_orange_circle_y(img1))
print("Image 2 orange circle top y=", find_orange_circle_y(img2))
