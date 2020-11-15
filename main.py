import PyPDF2
from gtts import gTTS
from time import sleep
import re
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Prerun code to clear files
directory = "./"
files_in_directory = os.listdir(directory)
filtered_files = [file for file in files_in_directory if file.endswith(".txt")]
print(filtered_files)
for file in filtered_files:
    path_to_file = os.path.join(directory, file)
    os.remove(path_to_file)

# creating a pdf file object
pdfFileObj = open('The-Compound-Effect.pdf', 'rb')
language = 'en'

# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
total = pdfReader.numPages

numOfChaps = int(input("Enter number of chapters: "))
pageNums = []
chapName = ["THE COMPOUND EFFECT"]

for i in range(numOfChaps):
    print("Chapter", i+1, "starts at", end="")
    pageNums.append(int(input(" : "))-1)


pageNums.append(total)
print("Converting pdf to files")

for j in range(len(pageNums)-1):

    for i in range(pageNums[j], pageNums[j+1]-1):
        pageText = pdfReader.getPage(i).extractText()
        chapter1 = open("chap"+str(j+1)+".txt", "a+",
                        encoding='utf-8', errors='ignore')
        chapter1.write(pageText)
        chapter1.close()

    # ------------------- Cleaning the text -------------------
    with open("./chap"+str(j+1)+".txt", "r", encoding='utf-8', errors='ignore') as file:
        with open("chap"+str(j+1)+"_cleaned.txt", "a+",  encoding='utf-8', errors='ignore') as chap1:
            for line in file:
                line = line.strip()

                # Removing extra lines coming from PyPDF2
                if(line.startswith("Chapter_"+str(j+1)+".indd")):
                    # line = file.readline()
                    continue
                if(re.search("^\d{1}\/\d{2}", line)):
                    # print("Found")
                    continue
                # Adding Chapter Names
                if(line.startswith("CHAPTER")):
                    chapName.append(line[9:].strip())
                    chap1.write(line[:9]+" "+line[9:]+"\n")
                    continue
                # Removing top line of chapter1 Name
                # if("THE COMPOUND EFFECT" in line):
                #     line = line[line.index(
                #         "THE COMPOUND EFFECT")+len("THE COMPOUND EFFECT"):]

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

# ------------------- Converting to voice -------------------
os.mkdir("Audios")
for j in range(len(pageNums)-1):
    with open("chap"+str(j+1)+"_cleaned.txt", encoding='utf-8', errors='ignore') as file:
        myobj = gTTS(text=file.read(), lang=language, slow=False)
        myobj.save("./Audios/chap"+str(j+1)+".mp3")
        sleep(1)
        print(str(j+1)+" audio file created")


# ---------------------- Code to upload audios to drive ------------------
print("Enter Drive Credentials")
# Below code does the authentication part of the code
gauth = GoogleAuth()

# Creates local webserver and auto handles authentication.
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)


path = os.path.join(os.getcwd(), "Audios")
# print(path)

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
f = None
print("Completed Uploading audio files to drive")

print("\nEnjoy your chapter wise audio book")
