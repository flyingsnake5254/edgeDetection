from PIL import Image, ImageOps, ImageFilter
import numpy as np
import math

mask = np.array([1, 2, 1])
threshold = 100
change = 255 / 1020

def getGx(left , right):
    global mask
    gx = abs(np.sum(mask * left) - np.sum(mask * right))

    return (int)(gx*change)


def getGy(top , bottom):
    global mask
    gy = abs(np.sum(mask * top) - np.sum(mask * bottom))
    return (int)(gy*change)

def getG(left , right , top , bottom):
    Gx = getGx(left , right)
    Gy = getGy(top , bottom)
    G = math.sqrt(Gx** 2 + Gy** 2)
    atan = 0
    if Gx == 0:
        if Gy > 0:
            atan = math.atan(float('inf'))
        else :
            atan = math.atan(-1 * float('inf'))
    else:
        atan = math.atan(Gy / Gx)
    return G , atan


path = 'D:\\agatha2.png'

img = Image.open(path)
img.show()
grayimg = ImageOps.grayscale(img)
grayimg.show()
grayimg.filter(ImageFilter.GaussianBlur(radius=5))
grayimg.show() # 高斯模糊
grayarr = np.array(grayimg)
grayarrX = np.array(grayimg)
grayarrY = np.array(grayimg)
grayarrG = np.array(grayimg)
theta = []
for i in range(grayarrG.shape[0]):
    l = []
    for i in range(grayarrG.shape[1]):
        l.append(0)
    theta.append(l)
theta = np.array(theta , np.float32)

for i in range(len(mask) // 2, grayarr.shape[0] - len(mask) // 2):
    for j in range(len(mask) // 2, grayarr.shape[1] - len(mask) // 2):

        left = np.array([grayarr[i - 1][j - 1],grayarr[i][j - 1],grayarr[i + 1][j - 1]])
        right = np.array([grayarr[i - 1][j + 1],grayarr[i][j + 1],grayarr[i + 1][j + 1]])
        top = np.array([grayarr[i - 1][j - 1], grayarr[i - 1][j], grayarr[i - 1][j + 1]])
        bottom = np.array([grayarr[i + 1][j - 1], grayarr[i + 1][j], grayarr[i + 1][j + 1]])

        grayarrX[i][j] = getGx(left , right)
        grayarrY[i][j] = getGy(top , bottom)

        grayarrG[i][j] , theta[i][j] = getG(left , right , top , bottom)

imgX = Image.fromarray(grayarrX)
imgY = Image.fromarray(grayarrY)
imgG = Image.fromarray(grayarrG)

# 非最大值抑制
arrNon = np.copy(grayarrG)
for i in range(len(mask) // 2, grayarr.shape[0] - len(mask) // 2):
    for j in range(len(mask) // 2, grayarr.shape[1] - len(mask) // 2):
        t = math.degrees(theta[i][j])
        pixel1 = 0
        pixel2 = 0
        G = grayarrG[i][j]
        # 垂直方向鄰近點
        if (t >= 67.5 and t <= 90) or (t <= -67.5 and t >= -90):
            pixel1 = grayarrG[i - 1][j]
            pixel2 = grayarrG[i + 1][j]

        # 斜對角(左下->右上)
        elif (t >= 22.5 and t <= 67.5):
            pixel1 = grayarrG[i - 1][j + 1]
            pixel2 = grayarrG[i + 1][j - 1]

        # 水平方向鄰近點
        elif (t >= -22.5 and t <= 22.5):
            pixel1 = grayarrG[i][j - 1]
            pixel2 = grayarrG[i][j + 1]

        # 斜對角(左上->右下)
        else:
            pixel1 = grayarrG[i - 1][j - 1]
            pixel2 = grayarrG[i + 1][j + 1]

        if G >= pixel1 and G >= pixel2:
            pass
        else:
            G = 0
        arrNon[i][j] = G

imgGNON = Image.fromarray(arrNon)

#雙閾值
strongPixel = np.copy(arrNon)
highThreshold = 30
lowThreshold = 10

for i in range(len(mask) // 2, grayarr.shape[0] - len(mask) // 2):
    for j in range(len(mask) // 2, grayarr.shape[1] - len(mask) // 2):
        pixel = arrNon[i][j]
        # 強像素
        if pixel > highThreshold:
            strongPixel[i][j] = 255
        # 抑制
        elif pixel < lowThreshold:
            strongPixel[i][j] = 0
        # 弱像素
        else:
            strongPixel[i][j] = 150

imgStrong = Image.fromarray(strongPixel)
imgStrong.show() # 雙閾值

#追蹤
for i in range(len(mask) // 2, grayarr.shape[0] - len(mask) // 2):
    for j in range(len(mask) // 2, grayarr.shape[1] - len(mask) // 2):
        nowPixel = strongPixel[i][j]
        if nowPixel == 150:
            strongPixel[i][j] = 0
            arround = [strongPixel[i-1][j-1],strongPixel[i-1][j],strongPixel[i-1][j+1]
                       ,strongPixel[i][j-1],strongPixel[i][j+1]
                       ,strongPixel[i+1][j-1],strongPixel[i+1][j],strongPixel[i+1][j+1]]

            for pixel in arround:
                if pixel == 255:

                    strongPixel[i][j] = 255
                    break

imgFinal = Image.fromarray(strongPixel)
# imgX.show()
# imgY.show()
imgG.show() #索伯算子
imgGNON.show() #抑制非最大值

imgFinal.show() # final
