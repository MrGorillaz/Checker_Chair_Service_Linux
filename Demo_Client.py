from shutil import copyfile

cases = {
    1:('CamParam - Blue.csv',"blau_cam0.jpg"),
    2:('CamParam - Blue2.csv',"blau_cam0.jpg"),
    3:('CamParam - Red.csv',"rot_cam0.jpg"),
    4:('CamParam - Red2.csv',"rot_cam0.jpg"),
    5:('CamParam - DarkBlue.csv',"Dunkelblau_cam0.jpg"),
    6:('CamParam - DarkBlue2.csv',"Dunkelblau_cam0.jpg"),
    7:('CamParam - Black.csv',"schwarz_cam0.jpg"),
    8:('CamParam - Black2.csv',"schwarz_cam0.jpg"),
    9:('CamParam - Black2.csv',"rot_cam0.jpg")
}

def set_check(paramfile,checkimage):
    defaultParamFile = 'CamParam.csv'
    sourceParamPath = 'ParamFiles/Test_Params/' + paramfile
    destinationParamPath = 'ParamFiles/' + defaultParamFile
    sourceImagePath = 'SourceImages/Test_Images/' + checkimage
    destinationPath = 'SourceImages/'+checkimage
    copyfile(sourceImagePath,destinationPath)
    copyfile(sourceParamPath,destinationParamPath)

#Welcome Screen
while True:
    print("### DEMO Program ###")
    print("Choose your Check:")
    print("1: Blue Basic")
    print("2: Blue Rulebased")
    print("3: Red Basic")
    print("4: Red Rulebased")
    print("5: Dark Blue Basic")
    print("6: Dark Blue Rulebased")
    print("7: Black Basic")
    print("8: Black Rulebased")
    print("9: Error")

    option = input("Option:")
    print("\n\nS")
    try:
        if int(option) in range(1,10):
            print(cases.get(int(option)))
            set_check(cases.get(int(option))[0],cases.get(int(option))[1])
        else:
            raise ValueError

    except ValueError:
        print("Wrong Intput\n\n")
