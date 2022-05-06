import cv2

# 讀取圖片並轉灰階
path = "D:\\conan.png"
oriImg = cv2.imread(path)
grayImg = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

maskSize = 5

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

