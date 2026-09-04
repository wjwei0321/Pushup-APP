from PIL import Image

img1 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788520200948.png")
img2 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788520200694.png")

def find_orange_text_top(img):
    w, h = img.size
    pix = img.load()
    for y in range(250, 400):
        # Scan across the width to find the orange text
        for x in range(30, 200):
            p = pix[x, y]
            if p[0] > 200 and p[1] > 100 and p[2] < 50:
                return y
    return -1
    
print("Image 1 orange text y=", find_orange_text_top(img1))
print("Image 2 orange text y=", find_orange_text_top(img2))
