from PIL import Image

img1 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788517336338.png")
img2 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788517336315.png")

def find_strive_text(img):
    w, h = img.size
    pix = img.load()
    for y in range(100, 200):
        for x in range(100, 200):
            p = pix[x, y]
            if 150 < p[0] < 170 and 150 < p[1] < 170 and 150 < p[2] < 170:
                return y
    return -1
    
print("Image 1 STRIVE text y=", find_strive_text(img1))
print("Image 2 STRIVE text y=", find_strive_text(img2))
