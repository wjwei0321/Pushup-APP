from PIL import Image

img1 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788517336338.png")
img2 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788517336315.png")

# find the Y coordinate of the "15" on the Y-axis of the chart in image 1
def find_y_axis_label(img):
    w, h = img.size
    pix = img.load()
    for y in range(300, 600):
        # Scan for black pixel on the left (Y axis labels are black/grey)
        for x in range(10, 50):
            p = pix[x, y]
            if p[0] < 50 and p[1] < 50 and p[2] < 50:
                return y
    return -1
    
print("Image 1 y-axis label y=", find_y_axis_label(img1))
print("Image 2 y-axis label y=", find_y_axis_label(img2))
