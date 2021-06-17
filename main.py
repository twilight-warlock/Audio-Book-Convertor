import PyPDF2
import pyttsx3
from time import sleep
import re
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import shutil

pageNums = []
# ----------------- Cleaning stage -------------------

def deleteFolders(directory,field):
    files_in_directory = os.listdir(directory)

    filtered_files = [file for file in files_in_directory if file.endswith(field)]

    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)
    
    os.removedirs(directory)

# Prerun code to clear files
def cleanUp():
    directory = [
        {"name":"data","fileType":".txt"}, 
        {"name":"Audios","fileType":".mp3"}, 
        ]

    for obj in directory:
        deleteFolders(obj["name"],obj["fileType"])


def textScrape():

    os.mkdir("data")
    # creating a pdf file object
    pdfFileObj = open('The-Compound-Effect.pdf', 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    total = pdfReader.numPages

    numOfChaps = int(input("Enter number of chapters: "))
    chapName = ["THE COMPOUND EFFECT"]

    for i in range(numOfChaps):
        print("Chapter", i+1, "starts at", end="")
        pageNums.append(int(input(" : "))-1)


    pageNums.append(total)
    print("Converting pdf to files")

    for j in range(len(pageNums)-1):

        for i in range(pageNums[j], pageNums[j+1]-1):
            pageText = pdfReader.getPage(i).extractText()
            chapter1 = open(os.path.join("data","chap"+str(j+1)+".txt"), "a+",
                            encoding='utf-8', errors='ignore')
            chapter1.write(pageText)
            chapter1.close()

        # ------------------- Cleaning the text -------------------
        with open(os.path.join("data","chap"+str(j+1)+".txt"), "r", encoding='utf-8', errors='ignore') as file:
            with open(os.path.join("data","chap"+str(j+1)+"_cleaned.txt"), "a+",  encoding='utf-8', errors='ignore') as chap1:
                for line in file:
                    line = line.strip()

                    # Removing extra lines coming from PyPDF2
                    if(line.startswith("Chapter_"+str(j+1)+".indd")):
                        continue
                    if(re.search("^\d{1}\/\d{2}", line)):
                        continue
                    # Adding Chapter Names
                    if(line.startswith("CHAPTER")):
                        chapName.append(line[9:].strip())
                        chap1.write(line[:9]+" "+line[9:]+"\n")
                        continue

                    if("Chapter_"+str(j+1)+".indd" in line):
                        line = line[:line.index("Chapter_"+str(j+1)+".indd")]

                    if re.search("\d{2} .M.+", line):
                        word = "AM" if "AM" in line else "PM"
                        for e in chapName:
                            if(e in line):
                                word = e
                                break
                        line = line[line.index(word)+len(word):]
                        if(line.isnumeric()):
                            continue

                    chap1.write(line+" ")
    pdfFileObj.close()
    print("Text cleaning finished")
    print("Starting the conversion to audio files")

# ---------------- Converting to voice -------------------
def textToVoice():
    engine = pyttsx3.init()
    os.mkdir("Audios")
    for j in range(len(pageNums)-1):
        with open(os.path.join("data","chap"+str(j+1)+"_cleaned.txt"), encoding='utf-8', errors='ignore') as file:
            engine.save_to_file(file.read(),os.path.join("Audios","chap"+str(j+1)+".mp3"))
            engine.runAndWait()
            sleep(1)
            print(str(j+1)+" audio file created")

# --------------- Code to upload audios to drive ------------------
def driveUploadAll():
    print("Enter Drive Credentials")

    # Below code does the authentication part of the code
    gauth = GoogleAuth()

    # Creates local webserver and auto handles authentication.
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)


    path = os.path.join(os.getcwd(), "Audios")

    # Creating a folder in drive
    folder = drive.CreateFile(
        {'title': "The Compound Effect", 'mimeType': 'application/vnd.google-apps.folder'})
    folder.Upload()
    print("Created Folder in drive")

    # iterating through all the files of the Audios directory
    for x in os.listdir(path):
        f = drive.CreateFile({'title': x, 'parents': [{'id': folder.get("id")}]})
        f.SetContentFile(os.path.join(path, x))
        f.Upload()
        print("Uploaded 1 file")
    f = None
    print("Completed Uploading audio files to drive")

    print("\nEnjoy your chapter wise audio book")

# --------------- Create a Zip file for audios (Optional) ------------------
def zipCreator():
    shutil.make_archive("Audios", 'zip', "Audios")
    print("Zip file created")

# --------------- Drive upload for Zip ---------------------------
def driveUploadZip():
    # Creating a folder in drive
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    folder = drive.CreateFile(
        {'title': "The Compound Effect Zip", 'mimeType': 'application/vnd.google-apps.folder'})
    folder.Upload()
    print("Created Folder in drive")

    f = drive.CreateFile({'title': "Audios", 'parents': [{'id': folder.get("id")}]})
    f.SetContentFile("Audios.zip")
    f.Upload()
    print("Uploaded 1 file")

def main():
    cleanUp()
    textScrape()
    textToVoice()
    zipCreator()
    driveUploadZip()
    driveUploadAll()

main()

# Input
# Enter number of chapters: 6
# Chapter 1 starts at : 25
# Chapter 2 starts at : 43
# Chapter 3 starts at : 75
# Chapter 4 starts at : 113
# Chapter 5 starts at : 139
# Chapter 6 starts at : 160