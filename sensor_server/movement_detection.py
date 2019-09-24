'''
    This class is resonsible for determining movement
    in the image using openCV functions.
'''

import cv2
import numpy as np
import time
from heat_map import HeatMap

class MovementDetection:

    def __init__(self, res_height, res_width, disp_height, disp_width, overlay_alpha = 0.35):

        #Move windows to better place
        cv2.namedWindow('Raw')
        cv2.moveWindow('Raw', 0, 0)
        #cv2.namedWindow('Gray')
        #cv2.moveWindow('Gray', 400, 0)
        #cv2.namedWindow('Gauss')
        #cv2.moveWindow('Gauss', 800, 0)
        #cv2.namedWindow('Delta')
        #cv2.moveWindow('Delta', 0, 350)
        #cv2.namedWindow('Threshold')
        #cv2.moveWindow('Threshold', 400, 350)
        cv2.namedWindow('Heat Map')
        cv2.moveWindow('Heat Map', 450, 300)
        cv2.namedWindow('Overlay')
        cv2.moveWindow('Overlay', 900, 0)

        #Prev grey frame for frame differences
        self.prev_gray = None

        #Set display size of heat map
        self.disp_height = disp_height
        self.disp_width = disp_width

        self.alpha = overlay_alpha

        #Create Heat Map
        self.heat_map = HeatMap(res_height, res_width)

    def process(self, img):

        frame0 = img

        #Grey image
        frame1 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)

        #Apply gaussian blur
        frame2 = cv2.GaussianBlur(frame1, (21, 21), 0)

        #Initialise prev_gray
        if self.prev_gray is None:
            self.prev_gray = frame2

        #Delta frame
        frame3 = cv2.absdiff(self.prev_gray, frame2)

        #Threshold frame
        frame4 = cv2.threshold(frame3, 15, 255, cv2.THRESH_BINARY)[1]

        #Increment tiles in heat map
        self.heat_map.increment_tiles(frame4)

        #Convert 16 bit int heat map to 8 bit int openCV image
        sixteen_bit_hm = self.heat_map.heat_map
        eight_bit_hm = cv2.convertScaleAbs(self.heat_map.heat_map, alpha=(255.0/65535.0))

        #Apply colour map to 8 bit int image
        frame5 = cv2.applyColorMap(eight_bit_hm, cv2.COLORMAP_JET)

        #Remove blue for overlay
        blue_mask= cv2.inRange(frame5, np.array([128,0,0]), np.array([128,0,0]))
        frame6 = frame5.copy()
        frame6[blue_mask>0] = frame0[blue_mask>0]

        #Apply overlay
        frame7 = frame5.copy()
        cv2.addWeighted(frame6, self.alpha, frame0 , 1-self.alpha, 0, frame7)

        #Update previous frame
        self.prev_gray = frame2

        #Display the images
        cv2.imshow('Raw', frame0)
        #cv2.imshow('Gray', frame1)
        #cv2.imshow('Gauss', frame2)
        #cv2.imshow('Delta', frame3)
        #cv2.imshow('Threshold', frame4)

        #Image can be resized beyond its actual resolution
        frame5_resized = cv2.resize(frame5, (self.disp_width, self.disp_height))
        frame7_resized = cv2.resize(frame7, (self.disp_width, self.disp_height))

        cv2.imshow('Heat Map', frame5_resized)
        cv2.imshow('Overlay', frame7_resized)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    #Changes heat map growth rate
    def increment_heat_map_growth_rate(self, amount):

        self.heat_map.increment_growth_rate(amount)

    #Changes heat map decay rate
    def increment_heat_map_decay_rate(self, amount):

        self.heat_map.increment_decay_rate(amount)

    #Resets growth and decay rates to default values
    def reset_heat_map_rates(self):

        self.heat_map.reset_rates()
