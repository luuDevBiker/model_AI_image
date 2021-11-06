import cv2
import numpy as np

# img = cv2.imread(r"D:/anhmau.jpg")
# img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#
# img = cv2.bitwise_not(img)
# th2 = cv2.adaptiveThreshold(img,255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,15,-2)
# cv2.imshow("th2", th2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# horizontal = th2
# vertical = th2
# rows,cols = horizontal.shape
#
# #inverse the image, so dat lines are black for masking
# horizontal_inv = cv2.bitwise_not(horizontal)
# #perform bitwise_and to mask the lines with provided mask
# masked_img = cv2.bitwise_and(img, img, mask=horizontal_inv)
# #reverse the image back to normal
# masked_img_inv = cv2.bitwise_not(masked_img)
# cv2.imshow("masked img", masked_img_inv)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# horizontalsize = int(cols / 30)
# horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalsize,1))
# horizontal = cv2.erode(horizontal, horizontalStructure, (-1, -1))
# horizontal = cv2.dilate(horizontal, horizontalStructure, (-1, -1))
# cv2.imshow("horizontal", horizontal)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# verticalsize = int(rows / 30)
# verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
# vertical = cv2.erode(vertical, verticalStructure, (-1, -1))
# vertical = cv2.dilate(vertical, verticalStructure, (-1, -1))
# cv2.imshow("vertical", vertical)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# vertical = cv2.bitwise_not(vertical)
# cv2.imshow("vertical_bitwise_not", vertical)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# #step1
# edges = cv2.adaptiveThreshold(vertical,255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3,-2)
# cv2.imshow("edges", edges)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# #step2
# kernel = np.ones((2, 2), dtype = "uint8")
# dilated = cv2.dilate(edges, kernel)
# cv2.imshow("dilated", dilated)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# # step3
# smooth = vertical.copy()
#
# #step 4
# smooth = cv2.blur(smooth, (4,4))
# cv2.imshow("smooth", smooth)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# #step 5
# (rows, cols) = np.where(img == 0)
# vertical[rows, cols] = smooth[rows, cols]
# cv2.imshow("vertical_final", vertical)

# Remove horizontal


cv2.waitKey(0)
cv2.destroyAllWindows()
path = r'1 (1).jpg'
image = cv2.imread(path)

print(image.shape)
W , H , C = image.shape
image = cv2.resize(image,( H // 2, W // 2))

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25,1))
detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    cv2.drawContours(image, [c], -1, (255,255,255), 10)
# Repair image
repair_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,6))
result = 255 - cv2.morphologyEx(255 - image, cv2.MORPH_CLOSE, repair_kernel, iterations=1)
kernel = np.ones((4,4), np.uint8)
image = cv2.erode(image,kernel,iterations=2)

cv2.imshow('image', image)
cv2.imshow('result', result)
cv2.waitKey()