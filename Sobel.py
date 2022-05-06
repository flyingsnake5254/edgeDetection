from PIL import Image, ImageOps
import numpy as np
import math

mask = np.array([1, 2, 1])
threshold = 150

def getGx(left , right):
    global mask
    gx = abs(np.sum(mask * left) - np.sum(mask * right))

    # set threshold
    if gx > threshold:
        return 255
    return 0


def getGy(top , bottom):
    global mask
    gy = abs(np.sum(mask * top) - np.sum(mask * bottom))
    #threshold
    if gy > threshold:
        return 255
    return 0

def getG(left , right , top , bottom):
    G = math.sqrt((getGx(left , right) ** 2 + getGy(top , bottom) ** 2))

    #set threshold
    if G > threshold:
        return 255
    return 0


path = 'D:\\school2.jpg'

img = Image.open(path)
grayimg = ImageOps.grayscale(img)

grayarr = np.array(grayimg)
grayarrX = np.array(grayimg)
grayarrY = np.array(grayimg)
grayarrG = np.array(grayimg)
for i in range(len(mask) // 2, grayarr.shape[0] - len(mask) // 2):
    for j in range(len(mask) // 2, grayarr.shape[1] - len(mask) // 2):
        left = np.array([grayarr[i - 1][j - 1],grayarr[i][j - 1],grayarr[i + 1][j - 1]])
        right = np.array([grayarr[i - 1][j + 1],grayarr[i][j + 1],grayarr[i + 1][j + 1]])
        top = np.array([grayarr[i - 1][j - 1], grayarr[i - 1][j], grayarr[i - 1][j + 1]])
        bottom = np.array([grayarr[i + 1][j - 1], grayarr[i + 1][j], grayarr[i + 1][j + 1]])

        grayarrX[i][j] = getGx(left , right)
        grayarrY[i][j] = getGy(top , bottom)
        grayarrG[i][j] = getG(left , right , top , bottom)

imgX = Image.fromarray(grayarrX)
imgY = Image.fromarray(grayarrY)
imgG = Image.fromarray(grayarrG)

imgX.show()
imgY.show()
imgG.show()