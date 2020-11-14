import PyPDF2
from gtts import gTTS

# creating a pdf file object
pdfFileObj = open('The-Compound-Effect.pdf', 'rb')
chapter1 = open("chap1.txt", "a+")

# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# Entering page numbers for each chapter (start,end+1)
for i in range(24, 42):
    pageText = pdfReader.getPage(i).extractText()
    chapter1.write(pageText)
    chapter1.write("\n\n\n")

pdfFileObj.close()
chapter1.close()

# ------------------- Cleaning the text -------------------
with open("./chap1.txt", "r") as file:
    with open("chap1_cleaned.txt", "a+") as chap1:
        for line in file:
            line = line.strip()

            # Removing extra lines coming from PyPDF2
            if(line.startswith("Chapter_1.indd")):
                line = file.readline()
                line = file.readline()
                line = file.readline()
                line = file.readline()
                line = file.readline()

            # Removing top line of Book Name
            if("THE COMPOUND EFFECT" in line):
                line = file.readline()
            chap1.write(line)

# ------------------- Converting to voice -------------------
with open("chap1_cleaned.txt") as file:
    language = 'en'
    myobj = gTTS(text=file.read(), lang=language, slow=False)
    myobj.save("chap1.mp3")

# import os
# os.remove("demofile.txt")
# os.mkdir()
# os.getcwd()
