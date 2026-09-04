from PIL import Image

img1 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788517336338.png")
img2 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788517336315.png")

def find_all_icon_bounds(img):
    w, h = img.size
    pix = img.load()
    icon_bounds = []
    
    # We know the icons are around y=750 to 900
    for x in range(0, w, 5):
        min_y = 1000
        max_y = 0
        for y in range(750, 900):
            p = pix[x, y]
            is_icon = p[0] < 250 or p[1] < 250 or p[2] < 250
            if is_icon:
                if y < min_y: min_y = y
                if y > max_y: max_y = y
        if max_y > min_y:
            icon_bounds.append((x, min_y, max_y))
            
    return icon_bounds

b1 = find_all_icon_bounds(img1)
b2 = find_all_icon_bounds(img2)
# print average min_y and max_y
print("Image 1:", sum([b[1] for b in b1])/max(1,len(b1)), sum([b[2] for b in b1])/max(1,len(b1)))
print("Image 2:", sum([b[1] for b in b2])/max(1,len(b2)), sum([b[2] for b in b2])/max(1,len(b2)))
