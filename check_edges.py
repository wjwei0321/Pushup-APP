from PIL import Image

img = Image.open(r"C:\Users\User\.gemini\antigravity\brain\4770aa3f-d7fa-442c-be50-2a738c41188b\.user_uploaded\media_1788516294533.jpg")
print("Size:", img.size)

# check edge pixels
pix = img.load()
print("Top left:", pix[0,0])
print("Bottom left:", pix[0, img.size[1]-1])
print("Bottom right:", pix[img.size[0]-1, img.size[1]-1])
