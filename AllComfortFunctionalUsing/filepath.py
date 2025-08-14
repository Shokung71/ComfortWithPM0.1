import os

def getFilepath():
    pathfile = input("Enter the path of file: ").strip('"').strip("'")

    filename = os.path.splitext(os.path.basename(pathfile))[0]
    print("\nThis filename will be:", filename)

    typefile = os.path.splitext(pathfile)[1].lower()
    print("\nThe type of the file is :", typefile)

    pathSave = os.path.dirname(pathfile)
    print("This program will saving file(s) into folder:", pathSave)

    return pathfile, filename, typefile, pathSave

# def pathSave():
#     pathSave = os.path.dirname(pathfile)