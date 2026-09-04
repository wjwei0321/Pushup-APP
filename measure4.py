from PIL import Image

img1 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788517336338.png")
img2 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788517336315.png")

def count_icons(img, y):
    w, h = img.size
    pix = img.load()
    icon_xs = []
    in_icon = False
    for x in range(w):
        p = pix[x, y]
        # Any non-white pixel
        is_icon = p[0] < 250 or p[1] < 250 or p[2] < 250
        if is_icon and not in_icon:
            icon_xs.append(x)
            in_icon = True
        elif not is_icon:
            in_icon = False
    return len(icon_xs), icon_xs

_, xs1 = count_icons(img1, 821)
_, xs2 = count_icons(img2, 819)

print("Image 1 icons at Y=821:", xs1)
print("Image 2 icons at Y=819:", xs2)
