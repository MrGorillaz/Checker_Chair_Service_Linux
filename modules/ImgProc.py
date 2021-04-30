##############################################
## Name:    result_handler                  ##
## Author:  Alexander Orlowski              ##
## Company: Sedus Sysems GmbH               ##
## Date:    28.07.2020                      ##
## Version: 0.5                             ##
##############################################
## Description:                             ##
## This Class is used for Image Processing  ##
## It handles HSV Conversion, ROI,          ##
## Image Reading & Preparation,             ##
## finding and counting contours.           ##
##############################################

import cv2
import os.path as path
import numpy as np

class ImProc:
    ## Constructor
    def __init__(self):
        lower_hsv = np.array([0, 0, 0])
        upper_hsv = np.array([0, 0, 0])
        width,heigth,channels = 0,0,0
        roi_start = (None)
        roi_end = (None)
        image = None
        debug = False

    #Private ErrorPrint Method
    def __errPrint(errortext):
        """
        Prints an Error-Message in RED to the Terminal
        :param errortext: Errortext you want to Display
        """
        CRED = '\033[91m'
        CEND = '\033[0m'
        print(CRED + 'ImProc_Error: '+errortext + CEND)

    # HSV Color Selection
    def setHSVcolor(self,hsv_low=np.array([0,0,0]),hsv_high=np.array([0,0,0]),color=None):
        #Check Color-Aliases
        if color not in ('red','blue','darkblue',None):
            self.__errPrint(str(color)+" is not in default Color-Range")

        # Set specified upper and lower HSV values
        if color is not None:
            if color == 'red':
                self.lower_hsv = np.array([0, 74, 0])
                self.upper_hsv = np.array([12, 206, 255])
            elif color == 'blue':
                self.lower_hsv = np.array([88, 149, 25])
                self.upper_hsv = np.array([136, 255, 255])
            elif color == 'darkblue':
                self.lower_hsv = np.array([93, 0, 0])
                self.upper_hsv = np.array([136, 255, 255])
        else:
            self.upper_hsv = hsv_high
            self.lower_hsv = hsv_low

    # Read and Prepare image
    def readImage(self,imagepath,roi_start=(None),roi_end=(None)):
        #read image
        if path.exists(imagepath):

            self.image = cv2.imread(imagepath)
            self.width, self.heigth, self.channels = self.image.shape
            if (type(roi_start) and type(roi_end)) and not (type([None])):
                print('ROI have to be a numpy Index')
            elif (len(roi_start) == len(roi_end)):
                self.setImageRoi(self,roi_start,roi_end)

        else:
            ImProc.__errPrint(imagepath+' not Found!')

    # Image Optimazation
    def setImageRoi(self,roi_start=(None),roi_end=(None),debug=False):
        self.image = self.image[roi_start[1]:roi_end[1],roi_start[0]:roi_end[0]]
        # Resize image to improve processing speed of Image
        self.image = cv2.resize(self.image, None, fx=0.2, fy=0.2)

        if (debug):
            cv2.imshow("test",self.image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    # Find and count Contours
    def findcontours(self,hsv_low=np.array([0,0,0]),hsv_high=np.array([0,0,0]),color=None,debug=False):

        if (color != None):
            self.setHSVcolor(self,color=str(color))

        elif((type(hsv_high) and type(hsv_low)) is type(np.array([]))) and ((hsv_low+hsv_high).all()):
            self.setHSVcolor(self,hsv_low=hsv_low,hsv_high=hsv_high)

        else:
            self.__errPrint('hsv_low or hsv_high dont seem to be Numpy_arrays')

        picHSV = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)        #convert image from RGB to HSV
        find = cv2.inRange(picHSV, self.lower_hsv, self.upper_hsv)  #Get HSV Pixel in HSV Range as Binary Image
        find = cv2.medianBlur(find, 15)                             #Blur image to reduce noise
        kernel = np.ones((9, 9), np.uint8)                          #Kernel for dilate
        deli = cv2.dilate(find, kernel, iterations=2)               #make HSV-Pixels bigger
        con, dump = cv2.findContours(deli, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  #get contours

        #draw Countours to screen
        if (debug):
            cv2.drawContours(self.image, con, -1, (0, 255, 0), 3)
            cv2.imshow("Found Contours", self.image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return len(con)









