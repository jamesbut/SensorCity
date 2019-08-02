import cv2
import numpy as np
import time
from heat_map import HeatMap

class MovementDetection:

    def __init__(self):

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
        self.prev_gray = None

        #Create Heat Map
        self.heat_map = HeatMap(240, 320, 16, 4)

    def process(self, img):

        frame0 = img

        #Grey image
        frame1 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)

        #Apply gaussian blur
        frame2 = cv2.GaussianBlur(frame1, (21, 21), 0)

        #Initialise prev_gray
        if self.prev_gray is None:
            self.prev_gray = frame2
            #continue

        #Delta frame
        frame3 = cv2.absdiff(self.prev_gray, frame2)

        #Threshold frame
        frame4 = cv2.threshold(frame3, 15, 255, cv2.THRESH_BINARY)[1]

        #Increment tiles in heat map
        self.heat_map.increment_tiles(frame4)
        frame5 = cv2.applyColorMap(self.heat_map.heat_map, cv2.COLORMAP_JET)
        print(self.heat_map.heat_map)

        #Update previous frame
        self.prev_gray = frame2

        #Display the images
        cv2.imshow('Raw', frame0)
        cv2.imshow('Gray', frame1)
        cv2.imshow('Gauss', frame2)
        cv2.imshow('Delta', frame3)
        cv2.imshow('Threshold', frame4)
        cv2.imshow('Heat Map', frame5)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
