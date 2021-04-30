##########################################
## Name:    HSV_Finder                  ##
## Author:  Alexander Orlowski          ##
## Company: Sedus Sysems GmbH           ##
## Date:    28.07.2020                  ##
## Version: 1.0
##########################################
## Description:                         ##
## This Program find and detect Objects ##
## given a picture based on its color   ##
##########################################

import cv2
import numpy as np
from sys import argv

#dummy funktion
def empty(a):
    pass

# Set Window for Trackbar for managing Values
cv2.namedWindow('ColorSelect')
cv2.createTrackbar('Hue_Low','ColorSelect',0,180,empty)
cv2.createTrackbar('Hue_High','ColorSelect',12,180,empty)
cv2.createTrackbar('Sat_Low','ColorSelect',74,255,empty)
cv2.createTrackbar('Sat_High','ColorSelect',206,255,empty)
cv2.createTrackbar('Val_Low','ColorSelect',0,255,empty)
cv2.createTrackbar('Val_High','ColorSelect',255,255,empty)


while True:
    # Get Values from Trackbar
    hue_low = cv2.getTrackbarPos('Hue_Low','ColorSelect')
    hue_high = cv2.getTrackbarPos('Hue_High','ColorSelect')
    sat_low = cv2.getTrackbarPos('Sat_Low','ColorSelect')
    sat_high = cv2.getTrackbarPos('Sat_High','ColorSelect')
    val_low = cv2.getTrackbarPos('Val_Low','ColorSelect')
    val_high = cv2.getTrackbarPos('Val_High','ColorSelect')

    #Read Image
    if ((len(argv) >1) and (argv[1] == '--picture') and (argv[2] != None)):
        pic = cv2.imread(argv[2].replace('/','//'))
    else:
        pic = cv2.imread('./SourceImages/Test_Images/Dunkelblau_cam0.jpg')
    #Resize Image for faster processing
    pic = cv2.resize(pic, None, fx=0.2, fy=0.2)
    #Change Color from RGB to HSV
    picHSV = cv2.cvtColor(pic, cv2.COLOR_BGR2HSV)

    #Set the lower and upper HSV-Ranges
    lower = np.array([hue_low,sat_low,val_low])
    upper = np.array([hue_high,sat_high,val_high])
    #Use OpenCV build-in inRange and medianBlur functions
    find = cv2.inRange(picHSV, lower, upper)
    #cv2.imshow('colorrange non Blur', find)
    find = cv2.medianBlur(find, 15)
    #cv2.imshow('colorrange with Blur', find)

    # Detect and draw contours
    kernel = np.ones((9, 9), np.uint8)
    deli = cv2.dilate(find, kernel, iterations=2)
    find = cv2.Canny(deli, 100, 200)
    con, dump = cv2.findContours(deli, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(pic, con, -1, (0, 255, 0), 3)

    #Write Text in Picture
    pic = cv2.rectangle(pic, (0, 0), (200, 50), (0, 0, 0), -1)
    pic = cv2.putText(pic, 'Found: ' + str(len(con)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('pic', pic)
    cv2.imshow('hsv', find)
    cv2.imshow('deli', deli)

    #will kill loop
    if (cv2.waitKey(25) > 0):
        cv2.destroyAllWindows()
        break
