# import the necessary packages
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
#call argument parse function
ap.add_argument("-v","--video",help="path to video")
#take video input
ap.add_argument("-a","--min-area", type=int,default=1500,help="minimum-area")
#define the max area
args = vars(ap.parse_args())
#actual argument passing, take in the variables(video) passed in the argument
vs = cv2.VideoCapture(args["video"])
#video capture saved in the variable vs
firstFrame=None

while True:
	frame = vs.read()
	#start reading the frames
	frame = frame if args.get('video',None) is None else frame[1]
	c#checks if frame was successfully grabbeddd
	if frame is None:
		break
	frame = imutils.resize(frame,width=500)
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)	
	#bgcolor grey for better recognizaton of object
	gray = cv2.GaussianBlur(gray,(21,21),0)
	#add guassian blurring to each frame, 21,21 kerne=l size 0 is sigma y
	if firstFrame is None:
		firstFrame = gray
		continue
	#delta=|initial_frame-modeled_frame|(pixels from)
	frameDelta = cv2.absdiff(firstFrame,gray)
	#first frame and gray's(our frame) absolute piixel difference
	thresh = cv2.threshold(frameDelta,25,255,cv2.THRESH_BINARY)[1]
	#binary threshold which checks if the value is less than 25 toh black otherwise whit inour frame
	thresh = cv2.dilate(thresh,None,iterations=2)
	cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	#contouring starts here.we take thresh copy as we used the dilated fuction but we want to keeppthe dilated values as they areso that we have one original version and use the copy to find contours.next is the cotour retrieval mode which finds the outermost puxels values.next functn simplifies the number to  simple value so that it can be easily processed.
	cnts = imutils.grab_contours(cnts)
	for c in cnts:
		if cv2.contourArea(c)< args["min_area"]:
			continue
		(x,y,w,h)=cv2.boundingRect(c)
		#we need a rectangle to be the bounding box hence
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,20),2)
		#starting pt of frame x,y...ending point, colour of bounding box, thickness
	cv2.imshow("Feed",frame)
	#window for video to play
	key = cv2.waitKey(2)
	#no of miliseconds the program should wait for the user to type in a key before automatically closing.
	if key== ord("q"):
	#it identifies q has been pressed and automatically stops the video and closes the window
		break
vs.release()
cv2.destroyAllWindows()
		
