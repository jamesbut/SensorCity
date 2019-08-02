import cv2
import numpy as np
import time
from heat_map import HeatMap

print(cv2.__version__)

cap = cv2.VideoCapture(0)

cap.set(3, 320)
cap.set(4, 240)

#I don't know why this has to be here but it
#seems essential for the delta frame to work
#time.sleep(0.5)

#Move windows to better place
cv2.namedWindow('Raw')
cv2.moveWindow('Raw', 0, 0)
cv2.namedWindow('Gray')
cv2.moveWindow('Gray', 400, 0)
cv2.namedWindow('Gauss')
cv2.moveWindow('Gauss', 800, 0)
cv2.namedWindow('Delta')
cv2.moveWindow('Delta', 0, 350)
cv2.namedWindow('Threshold')
cv2.moveWindow('Threshold', 400, 350)
cv2.namedWindow('Heat Map')
cv2.moveWindow('Heat Map', 800, 350)

#Prev grey frame for frame differences
prev_gray = None

#Create Heat Map
heat_map = HeatMap(240, 320)

while(True):

	#Read frame by frame
	retval, frame0 = cap.read();

	#Grey image
	frame1 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)

	#Apply gaussian blur
	frame2 = cv2.GaussianBlur(frame1, (21, 21), 0)

	#Initialise prev_gray
	if prev_gray is None:
		prev_gray = frame2
		continue

	#Delta frame
	frame3 = cv2.absdiff(prev_gray, frame2)

	#Threshold frame
	frame4 = cv2.threshold(frame3, 15, 255, cv2.THRESH_BINARY)[1]

	#Increment tiles in heat map
	heat_map.increment_tiles(frame4)
	frame5 = cv2.applyColorMap(heat_map.heat_map, cv2.COLORMAP_JET)
	print(heat_map.heat_map)

	#Update previous frame
	prev_gray = frame2

	#Display the images
	cv2.imshow('Raw', frame0)
	cv2.imshow('Gray', frame1)
	cv2.imshow('Gauss', frame2)
	cv2.imshow('Delta', frame3)
	cv2.imshow('Threshold', frame4)
	cv2.imshow('Heat Map', frame5)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

#When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
