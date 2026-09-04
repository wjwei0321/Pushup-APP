from PIL import Image

img1 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788517336338.png")
img2 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788517336315.png")

def find_large_number_top(img):
    w, h = img.size
    pix = img.load()
    for y in range(150, 400):
        # Scan across the width to find the large black text
        for x in range(30, 100):
            p = pix[x, y]
            # black text
            if p[0] < 20 and p[1] < 20 and p[2] < 20:
                return y
    return -1
    
print("Image 1 large number y=", find_large_number_top(img1))
print("Image 2 large number y=", find_large_number_top(img2))
