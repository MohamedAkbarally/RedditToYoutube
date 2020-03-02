from PIL import Image, ImageFont, ImageDraw
import textwrap
import os


def textToImage(text, id, isOP, folder):
    if isOP:
        img = Image.open("./Resources/backgrouda.png")
    else:
        img = Image.open("./Resources/backgroudq.png")


    lines = textwrap.wrap(text, width=100)
    newstr = "\n".join(lines)
    font = ImageFont.truetype("OpenSans.ttf", 32)

    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(newstr, font=font)
    w_floor = w
    if w < 1020:
        w_floor = 1020

    card_top = (1080-h)/2
    card_left = (1920-w_floor)/2
    card_bottom = card_top+h
    card_right = card_left+w_floor 

    #shadow
    shape = [(card_left-100, card_top-110), 
             (card_right+100+14,card_bottom+72+13)]
    draw.rectangle(shape, fill="#333333")

    #card
    shape = [(card_left-100, card_top-110), 
             (card_right+100, card_bottom+72)]
    draw.rectangle(shape, fill="#e8e8e8")

    #elipse
    elipseH =111*2
    eslipseW = 290
    elipse_top = ((1080-elipseH)/2) - (h+200)/2
    elipse_left = (1920-eslipseW)/2
    elipse_bottom = elipse_top+elipseH
    elipse_right =  elipse_left+eslipseW 
    shape = [(elipse_left, elipse_top),
             (elipse_right,elipse_bottom)]
    draw.ellipse(shape, fill="#e8e8e8")
    draw.text(((1920-w)/2, (1080-h)/2), newstr, font=font, fill="black")

    filename = "./raw/"+folder+"/"+id+".png"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    


    img.save(filename)

    return elipse_top
