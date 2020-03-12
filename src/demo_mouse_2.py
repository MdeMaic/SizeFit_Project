# import the necessary packages
from check_picture import obtainMeasures, resizeImg
from scipy.spatial import distance as dist
import argparse
import cv2

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False
def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, cropping
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		cropping = True
	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		refPt.append((x, y))
		cropping = False
		# draw a rectangle around the region of interest
		cv2.line(image, refPt[0], refPt[1], (0, 255, 0), 2)
		cv2.imshow("image", image)


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-a", "--altura", required=True, help="altura en centimetros")
args = vars(ap.parse_args())

# load the image, clone it, and setup the mouse callback function
image = args["image"]
altura = args["altura"]
#image,pix = obtainMeasures(image,altura)
#clone = image.copy()

#ACTUALMENTE
image = resizeImg(image)
pix = 1


if type(image) != bool:
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop)

    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF
        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
            image = image.copy()
        # if the 's' key is pressed, save the lines
        elif key == ord("s"):
            print("save")
        # if the 'c' key is pressed, break from the loop  
        elif key == ord("c"):
            break

    # if there are two reference points, then crop the region of interest
    # from teh image and display it
    if len(refPt) == 2:
        dpecho = dist.euclidean(refPt[0],refPt[1])
        realpecho = (dpecho/pix)*2*1.3
        cv2.putText(image,"{:.1f}cm".format(realpecho),(refPt[1][0]+10,refPt[1][1]+5),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0, 0, 255), 2)
        cv2.imshow("image", image)
        cv2.waitKey(0)
        #roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    
    elif len(refPt) == 4:
        dpecho = dist.euclidean(refPt[0],refPt[1])
        realpecho = (dpecho/pix)*2*1.3
        
        dcintura = dist.euclidean(refPt[2],refPt[3])
        realcintura = (dcintura/pix)*2*1.2
        
        cv2.putText(image,"{:.1f}cm".format(realpecho),(refPt[1][0]+10,refPt[1][1]+5),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0, 0, 255), 2)
        v2.putText(image,"{:.1f}cm".format(realcintura),(refPt[3][0]+10,refPt[3][1]+5),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0, 0, 255), 2)
        
        cv2.imshow("image", image)
        cv2.waitKey(0)

    #  close all open windows
    cv2.destroyAllWindows()
else:
    print("Please check and repeat it!")