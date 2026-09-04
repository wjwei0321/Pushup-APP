from PIL import Image

img1 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788517336338.png")

def find_y_axis_label(img):
    w, h = img.size
    pix = img.load()
    for y in range(300, 700):
        for x in range(10, 50):
            p = pix[x, y]
            if p[0] < 100 and p[1] < 100 and p[2] < 100:
                return y
    return -1
    
print("Image 1 y-axis label y=", find_y_axis_label(img1))
