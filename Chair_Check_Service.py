##########################################
## Name:    Chair_Check_Service         ##
## Author:  Alexander Orlowski          ##
## Company: Sedus Sysems GmbH           ##
## Date:    28.07.2020                  ##
## Version: 1.0                         ##
##########################################
## Description:                         ##
## This Program is as Proof of Concept  ##
## for Image Processing in QA.          ##
## It gets its Parameters over a CSV    ##
## and then Check if a given Image has  ##
## the wanted wheels.                   ##
##########################################
import modules.ImgProc as qa
import modules.handler.picture_handler as ph
import modules.handler.log_handler as lh
import modules.handler.result_handler as rh
import time
import os
from sys import argv
from pandas import read_csv

# CONSTANTS (literly)
#if argv[1] == '--debug':
#    DEBUG = True         #set True if you want to see what happens
#else:
DEBUG = False
ROI_START = (1,700) # start x,y pixel Value of ROI
ROI_END = (2400,1700) # end x,y pixel Value of ROI
WHEEL_COLORS = ('red','blue','darkblue')

# DEFAULTS
colorToFind = 'nope'
resultFileText = None
contours = 0

# DEFAULT FOLDERS
resultFolder = 'ResultFiles'
paramFolder = 'ParamFiles'
sourceImageFolder = 'SourceImages'
resultImageFolder = 'ResultImages'

# DEFAULT FILES
paramFile = 'CamParam.csv'
templateFile = 'Template_Results.csv'
sourceImageFile = 'cam0.jpg'

# DEFAULT PATHS
paramPath = paramFolder+'/'+paramFile
resultTemplatePath = resultFolder+'/'+templateFile
sourceImagePath = sourceImageFolder+'/'+sourceImageFile
resultImagePath = None

# SERVICE LOOP
ph.printlog('Service started....')

while (True):

    if(os.path.exists(paramPath)):
        # Get Parameters
        params = read_csv(paramPath, header=0, delimiter=';')
        results = read_csv(resultTemplatePath, header=0, delimiter=';')
        resultPath = resultFolder+'/'+params['NAME_ANTWORTFILE'][0]+'.csv'
        os.remove(paramPath)
        lh.printlog('Proceed: '+params['NAME_ANTWORTFILE'][0])

        #Take Image (picture)
        image = ph.take_picture(sourceImageFolder, sourceImageFile,debug=True)
        #Create Image Processing Object
        image_test = qa.ImProc
        # Read Image and set ROI
        image_test.readImage(image_test, image, ROI_START, ROI_END)

        try:
            #Checkrule for SALs
            if (params['X_SAL'][0] != '<NULL>'):
                lh.printlog('SAL - No Check needed')
                colorToFind = 'nope'
                contours = 5
            #Checkrule for Darkblue Wheels
            elif ((params['S_QS_ROLLE'][0] == 'DUNKELBLAU') or
                  (((params['S_MODELL'][0] == 'UP-133') or
                    (params['S_MODELL'][0] == 'SR-133')) and
                    (params['S_ZUSATZ_S_6001'][0] == 6001))):

                lh.printlog('Search for dark blue wheels')
                colorToFind = 'darkblue'

            #Checkrule for Black Wheels
            elif ((params['S_QS_ROLLE'][0] == 'SCHWARZ') or (params['S_STANDARD_2800'][0] == 2800) or
                  (params['S_STANDARD_2801'][0] == 2801) or (params['S_STANDARD_2802'][0] == 2802) or
                  (params['S_ZUSATZ_S_6201'][0] == 6201) or (params['S_ZUSATZ_S_6202'][0] == 6202) or
                  (params['S_ZUSATZ_S_6226'][0] == 6226) or (params['S_MODELL'][0] == 'NW-223') or
                  (params['S_MODELL'][0] == 'US-201') or (params['S_MODELL'][0] == 'MT-203') or
                  (params['S_ROLLE_GLEITER'][0] == 2800) or (params['S_ROLLE_GLEITER'][0] == 2801) or
                  (((params['S_MODELL'][0] == 'NW-100') or (params['S_MODELL'][0] == 'NW-199') or
                    (params['S_MODELL'][0] == 'YA-100') or (params['S_MODELL'][0] == 'MT-201') or
                    (params['S_MODELL'][0] == 'YA-102')) and (params['S_FUSS'][0] == 2401))):

                lh.printlog('Search for black wheels')
                colorToFind = 'black'

            #Checkrule for Red Wheels
            elif ((params['S_QS_ROLLE'][0] == 'ROT') or ((((params['S_STANDARD_2700'][0] == '2700') or
                  (params['S_ROLLE_GLEITER'][0] == 2700)) and (params['S_ZUSATZ_S_6226'][0] == '<NULL>')) or
                  ((params['S_ZUSATZ_S_6001'][0] == '<NULL>') and (params['S_ZUSATZ_S_6200'][0] == '<NULL>') and
                   (params['S_ZUSATZ_S_6201'][0] == '<NULL>') and (params['S_ZUSATZ_S_6202'][0] == '<NULL>') and
                   (params['S_ZUSATZ_S_6226'][0] == '<NULL>') and (params['S_ROLLE_GLEITER'][0] == '<NULL>') and
                   (params['S_STANDARD_2704'][0] == '<NULL>')))):

                colorToFind = 'red'
                lh.printlog('Search for red wheels')

            #Checkrule for Blue Wheels
            elif ((params['S_QS_ROLLE'][0] == 'BLAU') or
                  (((params['S_ZUSATZ_S_6001'][0] == 6001) or (params['S_MODELL'][0] == 'TU-181') or
                    (params['S_STANDARD_2704'][0] == 2704) or (params['S_ROLLE_GLEITER'][0] == 2701)) and
                     params['S_ZUSATZ_S_6226'][0] == '<NULL>') and (params['S_ROLLE_GLEITER'][0] == '<NULL>')):
                lh.printlog('Search for blue wheels')
                colorToFind = 'blue'

            #Who need wheels anyway -\_(°_°)_/-
            else:
                colorToFind = 'nope'

        #Catch KeyErrors if CSV is invalid
        except KeyError as err:
            lh.printlog('Error in PARAMFILE handling: ' + str(err))
            lh.writelog('Error in PARAMFILE handling: ' + str(err))
            lh.printlog('Aborting CHECK')
            resultImage = resultImageFolder + '/Fault/' + str(time.strftime("%Y_%m_%y__%H_%M_%S_") + image[-8:])
            results['FEHLERTEXT'] = ['PARAMFILE_FAULT']
            colorToFind = 'nope'

        # Count contours found
        try:
            if (colorToFind in WHEEL_COLORS):
                contours = image_test.findcontours(image_test, color=colorToFind, debug=DEBUG)
                lh.printlog(colorToFind + ' : ' + str(contours) + ' of 5 found!')

            #Special checkroutine for Black wheels
            elif(colorToFind == 'black'):

                for colors in WHEEL_COLORS:
                    contours = image_test.findcontours(image_test, color=colors, debug=DEBUG)

                    if contours >=2:
                        lh.printlog('wrong wheels found: '+str(contours)+' of 5 '+str(colors))
                        lh.writelog('wrong wheels found: '+str(contours)+' of 5 '+str(colors))
                        results['FEHLERTEXT'] = [str(colors + '_FOUND IN BLACK_FAULT')]
                        contours = 0
                        break
                    else:
                        contours = 5
            #Check OK
            if ((contours >= 2) or (colorToFind == 'nope')):
                lh.printlog('Check OK!')
                resultImage = resultImageFolder + '/' + str(time.strftime("%Y_%m_%y__%H_%M_%S_")+image[-8:])
                resultFileText = 'Check OK'

            #Check Not OK
            else:
                lh.printlog('Check NOT OK!')
                lh.writelog(str(params['NAME_ANTWORTFILE'][0]) +'_' + str(colorToFind) + '_FAULT')
                resultImage = resultImageFolder + '/Fault/' + str(time.strftime("%Y_%m_%y__%H_%M_%S_") + image[-8:])
                resultFileText = 'Check NOT OK'
                results['FEHLERTEXT'] = [str(colorToFind+'_FAULT')]

        #Catch Errors
        except NameError as err:
            lh.printlog('Error in Contour handling: '+str(err))
            lh.writelog('Error in Contour handling: '+str(err))
            lh.printlog('Aborting CHECK')
            resultImage = resultImageFolder + '/Fault/' + str(time.strftime("%Y_%m_%y__%H_%M_%S_") + image[-8:])
            results['FEHLERTEXT'] = ['PARAMFILE_FAULT']

        #Set Results
        results['CAM0'] = [resultImage]
        results['ERGEBNIS'] = [resultFileText]

        if (DEBUG):
            rh.set_results(params,results)
            rh.print_results(results)
        else:
            rh.write_results(params,results,resultPath)

        ph.move(image, resultImage)

        # VAR-Reset
        results     = None
        params      = None
        resultPath  = None
        colorToFind = 'nope'
        contours    = 0

    else:
        print('Waitng for Paramfile....')
        while (not os.path.exists(paramPath)):
            time.sleep(0.5)
