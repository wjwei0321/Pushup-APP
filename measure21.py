from PIL import Image

img2 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788520200694.png")

def find_grey_icon_1_x(img):
    w, h = img.size
    pix = img.load()
    for x in range(30, 100):
        # Scan column by column to find the first grey pixel in the 1st row (around y=788)
        for y in range(760, 810):
            p = pix[x, y]
            if 140 < p[0] < 160 and 140 < p[1] < 160 and 140 < p[2] < 160:
                return x
    return -1

print("Image 2 grey icon 1 X=", find_grey_icon_1_x(img2))
