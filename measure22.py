from PIL import Image

img1 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788520200948.png")
img2 = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788520200694.png")

def find_s_button(img):
    w, h = img.size
    pix = img.load()
    for y in range(200, 300):
        # Scan on the right side for the circular toggle
        for x in range(300, w-30):
            p = pix[x, y]
            if 200 < p[0] < 220 and 200 < p[1] < 220 and 200 < p[2] < 220:
                return y
    return -1

print("Image 1 S button y=", find_s_button(img1))
print("Image 2 S button y=", find_s_button(img2))
