##########################################
## Name:    result_handler              ##
## Author:  Alexander Orlowski          ##
## Company: Sedus Sysems GmbH           ##
## Date:    28.07.2020                  ##
## Version: 0.8
##########################################
## Description:                         ##
## This Module is for handling logs     ##
##########################################

from time import strftime
import sys

def printlog (msg):
    print(strftime("%d.%m.%Y %H:%M:%S"),'-',msg)

def writelog (msg,destination=''):
    original_stdout = sys.stdout  # Save a reference to the original standard output

    if destination == '':
        destination = strftime("%Y_%m_%d.log")

    with open(destination, 'a') as f:
        sys.stdout = f  # Change the standard output to the file we created.
        print(strftime("%d.%m.%Y %H:%M:%S"),'-',msg)
        sys.stdout = original_stdout  # Reset the standard output to its original value
        f.close()

#Write Logentries to a database
#Future Feature
def writeDB (msg,server,db,user,password,connector):
    pass

