from PIL import Image

img1 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788520200948.png")
img2 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788520200694.png")

def find_range_toggles_bottom(img):
    w, h = img.size
    pix = img.load()
    for y in range(400, 200, -1):
        # Scan for the 'S', 'M', 'L' buttons which are circles on the right side
        for x in range(300, 380):
            p = pix[x, y]
            # Orange background or grey outline
            if (p[0] > 200 and p[1] > 100 and p[2] < 50) or (150 < p[0] < 200 and 150 < p[1] < 200 and 150 < p[2] < 200):
                return y
    return -1

print("Image 1 range toggles bottom y=", find_range_toggles_bottom(img1))
print("Image 2 range toggles bottom y=", find_range_toggles_bottom(img2))
