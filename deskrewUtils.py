# import the necessary packages
import numpy as np
import argparse
import cv2
import imutils
from cv2 import WINDOW_NORMAL


def deskrew(src):
	image = cv2.imread(src)
	# image = imutils.resize(image, height = height)

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.bitwise_not(gray)
	thresh = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

	coords = np.column_stack(np.where(thresh > 0))

	rect = cv2.minAreaRect(coords)
	box = np.int0(cv2.boxPoints(rect))

	angle = cv2.minAreaRect(coords)[-1]
	print("Angle1:", angle)
	if box[0][1] > 200 or box[0][1] > box[1][1]:
		# Clockwise
		if angle < 45:
			angle = 90 - angle
		elif 88 <= angle <= 90:
			angle = angle
		else:
			angle = 90 - angle
	else:
		# Counter clockwise
		if angle < 45:
			angle = - angle
		elif 88 <= angle <= 90:
			angle = angle
		else:
			angle = - angle

	print("Angle2:", angle)
	(h, w) = image.shape[:2] # 0,1
	center = (w // 2, h // 2)
	M = cv2.getRotationMatrix2D(center, angle, 1.0)
	rotated = cv2.warpAffine(image, M, (w, h),
		flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
	cv2.waitKey(0)

	print("[INFO] angle: {:.3f}".format(angle))

	# cv2.imshow("Rotated", rotated)
	cv2.imwrite("rotated.jpg", rotated)
	# cv2.waitKey()
