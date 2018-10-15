from fnmatch import fnmatch
from os import path, makedirs, listdir
from PIL import Image, ImageShow, ImageOps

inputDir = r"InputImages"
outputDir = r"OutputImages"

inputImages =  [path.join(inputDir, x) for x in listdir(inputDir) if fnmatch(x, "*.png")]

if not path.exists(outputDir):
        makedirs(outputDir)  

for imagePath in inputImages:
    print("Processing: " + imagePath)
    fileName = path.basename(imagePath)
    img = Image.open(imagePath)
    outImg = ImageOps.expand(img, border=4, fill='black')
    outImg.save(path.join(outputDir, fileName)) #, quality=85
