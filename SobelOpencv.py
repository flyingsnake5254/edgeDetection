import cv2

# 讀取圖片並轉灰階
path = "D:\\el\\chung3_3.png"
oriImg = cv2.imread(path)
# oriImg = cv2.resize(oriImg, (500, 700), interpolation=cv2.INTER_AREA)
grayImg = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
# grayImg = cv2.resize(grayImg, (500, 700), interpolation=cv2.INTER_AREA)

maskSize = 3

ximg = cv2.Sobel(grayImg , cv2.CV_16S , 1 , 0 , maskSize)
yimg = cv2.Sobel(grayImg , cv2.CV_16S , 0 , 1 , maskSize)

# 將圖片轉成 unit 8
ximg = cv2.convertScaleAbs(ximg)
yimg = cv2.convertScaleAbs(yimg)

# 合併 X、 Y
outputImg = cv2.addWeighted(ximg , 0.5 , yimg , 0.5 , 0)

cv2.imshow("original image", oriImg)
cv2.imshow("Gx" , ximg)
cv2.imshow("Gy" , yimg)
cv2.imshow("sobel edge detection" , outputImg)

cv2.waitKey(0)
cv2.destroyAllWindows()

