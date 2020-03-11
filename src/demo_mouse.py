from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
from imageProcessing import resizeImg, generateMask
import numpy as np
import argparse
import imutils
import cv2


events = [i for i in dir(cv2) if 'EVENT' in i]
print (events)

# mouse callback function
def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img,(x,y),200,(255,0,0),2)

# Create a black image, a window and bind the function to window
img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)
while(1):
    cv2.imshow('image',img)
    if cv2.waitKey(20000):
        break
cv2.destroyAllWindows()