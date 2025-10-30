from icoextract import IconExtractor, IconExtractorError
from PIL import Image
import glob
import os
import re

print("hello world")
destination = "/media/luukie13/gaymes/Downloads/SteamIcons/" #where you want the icons saved to
sourcepath = "/media/luukie13/gaymes/SteamLibrary/steamapps/" #where your games are
#desktoppath = "/media/luukie13/gaymes/scripts/test/"
desktoppath = "/home/luukie13/.local/share/applications/" #this needs to go specifically here
game = "" 
gameID = ""
gameList = []

for folder in os.listdir(sourcepath + "common/"):
    if (os.path.isdir(sourcepath + "common/" + folder)):
        game = folder

        destination2 = destination + game + ".ico"
        destination3 = destination + game + ".png"
        path = sourcepath + "common/" + game + "/*.exe"
        altpath = sourcepath + "common/" + game + "/Game" + "/*.exe" #look this is just how fromsoft does it I guess

        if (glob.glob(path)): 
            path2 = glob.glob(path)[0]
        else:
            if (glob.glob(altpath)):
                path2 = glob.glob(altpath)[0]
            else:
                continue

        try:
            extractor = IconExtractor(path2)
            #extractor.export_icon(destination2, num=0) #if you just wanted to save the icon
            data = extractor.get_icon(num=0)
            with Image.open(data) as im:
                im.save(destination3)
            gameList.append(game)
            
        except IconExtractorError:
            print("shucks")
            pass

search = sourcepath + "appmanifest_*.acf"
manifests = glob.glob(search)
manifestList = []

for x in manifests:
    with open(x, "r") as f:
        for line in f:
            if "installdir" in line:
                newName = re.split("\"", line)
                gameID = re.split("_", x)[1][:-4]
                manifestList.append((newName[3], gameID))

for folder in os.listdir(sourcepath + "common/"):
    if (folder in gameList):
        game = folder
        desktopfile = desktoppath + game + ".desktop"
        destination3 = destination + game + ".png"

        for x in manifestList:
            if (x[0] == game):
                gameID = x[1]

        with open(desktopfile, "w") as f:
            f.write(
                "[Desktop Entry]" +
                "\nName=" + game +
                "\nExec=steam steam://rungameid/" + gameID +
                "\nType=Application" +
                "\nIcon=" + destination3 +
                "\nCategories=Game;" +
                "\nTerminal=false" +
                "\nStartupWMClass=steam_app_" + gameID +
                "\nComment=Play " + game + " on Steam"
                    )
