from PIL import Image

img1 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788520200948.png")
img2 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788520200694.png")

def find_grey_icon_row1(img):
    w, h = img.size
    pix = img.load()
    for y in range(700, 850):
        # Scan for grey icon pixels
        for x in range(30, w-30):
            p = pix[x, y]
            if 140 < p[0] < 160 and 140 < p[1] < 160 and 140 < p[2] < 160:
                return y
    return -1

print("Image 1 grey icon Row 1 y=", find_grey_icon_row1(img1))
print("Image 2 grey icon Row 1 y=", find_grey_icon_row1(img2))
