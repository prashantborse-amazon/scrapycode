import os
urlFilePath = os.path.join(os.getcwd(), "lambdaScraper/spiders/urls.txt")
with open(urlFilePath, 'r') as f:
    urlFile = f.readlines()

linesPerFile = 100
filenameCount = 1
for i in range(0, len(urlFile), linesPerFile):
    filePath = os.path.join(
        os.getcwd(), f"lambdaScraper/urls/load-urls_{filenameCount}.txt")
    with open(filePath, 'w+') as f:
        f.writelines(urlFile[i:i+linesPerFile])
    filenameCount += 1
