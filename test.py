import cv2
import time
import numpy as np

img = cv2.imread("D:\\conan.jpg", cv2.IMREAD_GRAYSCALE)

maskSize = 3
x = cv2.Sobel(img, cv2.CV_16S, 1, 0 ,3)
y = cv2.Sobel(img, cv2.CV_16S, 0, 1,3)

absX = cv2.convertScaleAbs(x)# 轉回uint8
absY = cv2.convertScaleAbs(y)

dst = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)

cv2.imshow("orign", img)
cv2.imshow("absX", absX)
cv2.imshow("absY", absY)

cv2.imshow("Result", dst)

# cv2.imwrite("D:\\schoolx.jpg" , absX)
# cv2.imwrite("D:\\schooly.jpg" , absY)
# cv2.imwrite("D:\\schoolc.jpg" , dst)

cv2.waitKey(0)
cv2.destroyAllWindows()

