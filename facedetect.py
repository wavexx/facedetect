#!/usr/bin/env python
import cv2
import string
import sys

ifn = sys.argv[1]
ofn = sys.argv[2]

im = cv2.equalizeHist(cv2.imread(ifn, cv2.IMREAD_GRAYSCALE))
cc = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
#cc = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_eye_tree_eyeglasses.xml')
#cc =
#cv2.CascadeClassifier('/usr/share/opencv/lbpcascades/lbpcascade_frontalface.xml')
flags = 0 # | cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT
detected = cc.detectMultiScale(im, 1.1, 4, flags, (50, 50))
for face in detected:
    cv2.rectangle(im, (face[0], face[1]), (face[0] + face[2], face[1] + face[3]), (255, 0, 0), 3)
cv2.imwrite(ofn, im)
