from PIL import Image
from PIL import ImageOps
import os

for file in os.listdir("player"):
    image = Image.open("player/" + file)

    splitname = file.split("-")
    filename = splitname.pop()
    splitname.pop(0)

    foldername = "-".join(splitname)

    os.makedirs("player/" + foldername, exist_ok=True)
    image.save("player/" + foldername + "/" + filename)
