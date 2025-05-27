from PIL import Image
import os


def resize(background, overlay): 
    bg_width, bg_height = background.size 
    new_overlay_width = int(bg_width * 0.20)
    new_overlay_height = int(bg_height * 0.2) 

    resized_overlay = overlay.resize((new_overlay_width, new_overlay_height))

    return resized_overlay

def addSign(background, overlay, ind):
    background.paste(resize(background, overlay), (900, 1130), resize(background, overlay))

    # Show the image
    background.show()

    name = "output" + str(ind) + ".png"

    background.save(name) 

def iterate(folder_path, overlay): 
    ind = 0
    for fileName in os.listdir(folder_path): 
        background = Image.open(folder_path + fileName)
        addSign(background, overlay, ind)
        ind = ind + 1



folder_path = "./Slides/"
overlay = Image.open("Signature.png")

iterate(folder_path, overlay)
# for fileName in os.listdir(folder_path): 
#     print(fileName)
