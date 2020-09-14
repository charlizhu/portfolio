# Some random image editing experimentation

from cv2 import *
import time

filename = "myFile3.jpg"

cam = VideoCapture(0)   # 0 -> index of camera
s, img = cam.read()
if s:    # frame captured without any errors
    namedWindow("cam-test")
    imshow("cam-test",img)
    time.sleep(1.5)
    waitKey(0)
    destroyWindow("cam-test")
    imwrite(filename,img) #save image

from PIL import Image, ImageDraw, ImageFont

image = Image.open(filename)

draw = ImageDraw.Draw(image)

font = ImageFont.truetype('ComicNeue-Bold.ttf', size=45)
(x, y) = (50, 950)
message = "hello frens \n\n i made dis \n  using pithom"
color = 'rgb(255, 69, 0)'

draw.text((x, y), message, fill=color, font=font)

im = Image.open(r"C:\Users\Linda.Zhang\PycharmProjects\stocks\ussr.jpg")
region = im.crop((0, 300, 450, 650))

image.paste(region, (0, 300, 450, 650))

image.save(filename,optimize=True, quality=50)
