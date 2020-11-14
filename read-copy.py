import PyPDF2
from gtts import gTTS
from time import sleep
# # creating a pdf file object
# pdfFileObj = open('The-Compound-Effect.pdf', 'rb')
language = 'en'
# # chapter1 = open("chap1.txt", "a+", encoding='utf-8', errors='ignore')

# # creating a pdf reader object
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
# total = pdfReader.numPages

# numOfChaps = int(input("Enter number of chapters: "))
# pageNums = []

# for i in range(numOfChaps):
#     print("Chapter", i+1, "starts at", end="")
#     pageNums.append(int(input(" : "))-1)


# pageNums.append(total)
# print(pageNums)

# for j in range(len(pageNums)-1):

#     for i in range(pageNums[j], pageNums[j+1]-1):
#         pageText = pdfReader.getPage(i).extractText()
#         chapter1 = open("chap"+str(j+1)+".txt", "a+",
#                         encoding='utf-8', errors='ignore')
#         chapter1.write(pageText)
#     # chapter1.close()
#     # ------------------- Cleaning the text -------------------
#     with open("./chap"+str(j+1)+".txt", "r", encoding='utf-8', errors='ignore') as file:
#         with open("chap"+str(j+1)+"_cleaned.txt", "a+",  encoding='utf-8', errors='ignore') as chap1:
#             for line in file:
#                 line = line.strip()

#                 # Removing extra lines coming from PyPDF2
#                 if(line.startswith("Chapter_1.indd")):
#                     line = file.readline()
#                     line = file.readline()
#                     line = file.readline()
#                     line = file.readline()
#                     line = file.readline()

#                 # Adding Chapter Names
#                 if(line.startswith("CHAPTER")):
#                     chap1.write(line[:9]+" "+line[9:]+"\n")
#                     continue
#                 # Removing top line of chapter1 Name
#                 if("THE COMPOUND EFFECT" in line):
#                     line = file.readline()
#                 chap1.write(line)
# pdfFileObj.close()


# ------------------- Converting to voice -------------------
for j in range(1, 6):
    with open("chap"+str(j+1)+"_cleaned.txt", encoding='utf-8', errors='ignore') as file:
        language = 'en'
        myobj = gTTS(text=file.read(), lang=language, slow=False)
        myobj.save("chap"+str(j+1)+".mp3")
        sleep(1)
        print(str(j+1)+" audio file created")
