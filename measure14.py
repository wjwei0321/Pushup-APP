from PIL import Image

img1 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788520200948.png")
img2 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788520200694.png")

def find_x_axis_label(img):
    w, h = img.size
    pix = img.load()
    for y in range(650, 750):
        # Scan for dark grey text around x=30 (the "4/12" label)
        for x in range(10, 50):
            p = pix[x, y]
            if 100 < p[0] < 150 and 100 < p[1] < 150 and 100 < p[2] < 150:
                return y
    return -1

print("Image 1 X-axis label y=", find_x_axis_label(img1))
print("Image 2 X-axis label y=", find_x_axis_label(img2))
