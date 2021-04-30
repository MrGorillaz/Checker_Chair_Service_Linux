##########################################
## Name:    picture_handler             ##
## Author:  Alexander Orlowski          ##
## Company: Sedus Sysems GmbH           ##
## Date:    28.07.2020                  ##
## Version: 0.8
##########################################
## Description:                         ##
## This Module is for handling          ##
## images                               ##
##########################################

import glob
from time import sleep
from modules.handler.log_handler import printlog
from shutil import move
import os.path as path

def take_picture (path,image,debug=False):

    if (debug==False):
        # this is only a POC placeholder routine
        # Cameraintegration for Basler-Cameras or other industrial cameras could be
        # implemented in the future with this method
        # e.g os.system(command)
        pass
    else:
        ImagePath = path + '/*' + image
        printlog('Waiting for Image to be taken...')
        while True:
            pic = glob.glob(ImagePath)
            if len(pic):
                printlog('Image had been taken')
                # sleep because otherwise the Attributes of the file are missing
                # and programm crashes
                sleep(0.1)
                return pic[0]

def move_picture (source,destination):

    if(path.exists(source) and path.exists(destination)):
        printlog('Image saved as ' + destination)
        move(source, destination)
    else:
        printlog('Error')



