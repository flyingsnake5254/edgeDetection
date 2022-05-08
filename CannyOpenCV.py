import cv2

image = cv2.imread('D:\\arthur.jpg')
# image = cv2.resize(image, (500, 700), interpolation=cv2.INTER_AREA)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3,3), 0)
canny = cv2.Canny(blurred, 50, 150)

cv2.imshow('Input', image)
cv2.moveWindow('Input' , 100 , 100)

cv2.imshow('Result', canny)
cv2.moveWindow('Result' , 200 , 200)

cv2.waitKey(0)
cv2.destroyAllWindows()