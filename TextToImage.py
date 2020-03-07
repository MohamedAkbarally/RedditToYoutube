from PIL import Image, ImageFont, ImageDraw
import textwrap
import os


def textToImage(text, id, isOP, folder,part,fulltext):

    #Selects the background of the image
    if isOP:
        img = Image.open("./Resources/backgrouda.png")
    else:
        img = Image.open("./Resources/backgroudq.png")

    lines = textwrap.wrap(text, width=60)
    newstr = "\n".join(lines)

    linesfull = textwrap.wrap(fulltext, width=60)
    stringfull = "\n".join(linesfull)

    font = ImageFont.truetype("./Resources/OpenSans.ttf", 55)

    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(stringfull, font=font)
    w_floor = w
    if w < 1020:
        w_floor = 1020

    card_top = (1080-h)/2
    card_left = (1920-w_floor)/2
    card_bottom = card_top+h
    card_right = card_left+w_floor 

     #elipse
    elipseH =111*2
    elipse_offset = elipseH/4
    eslipseW = 290
    elipse_top = ((1080-elipseH)/2) - (h+200)/2
    elipse_left = (1920-eslipseW)/2
    elipse_bottom = elipse_top+elipseH
    elipse_right =  elipse_left+eslipseW

    shape_shadow = [(elipse_left, elipse_top+elipse_offset),
             (elipse_right+9,elipse_bottom+elipse_offset)]
    draw.ellipse(shape_shadow, fill="#383838")

    shape = [(elipse_left, elipse_top+elipse_offset),
             (elipse_right,elipse_bottom+elipse_offset)]
    draw.ellipse(shape, fill="#000000")

    #shadow
    shape = [(card_left-100, card_top-110+elipse_offset), 
             (card_right+100+9,card_bottom+72+9+elipse_offset)]
    draw.rectangle(shape, fill="#383838")

    #card
    shape = [(card_left-100, card_top-110+elipse_offset), 
             (card_right+100, card_bottom+72+elipse_offset)]
    draw.rectangle(shape, fill="#000000")

   

    draw.text(((1920-w)/2, (1080-h)/2+elipse_offset), newstr, font=font, fill="white",align='left')

    filename = "./raw/"+folder+"/"+id+"_"+part+".png"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    img.save(filename)

    return elipse_top+elipse_offset



def AMAThumbnail(text, episode):

    #max length of title text
    if len(text)> 124:
        text = text[:124]+"..."

    
    img = Image.open("./Resources/thumbnail/bg.png")
    AMAlogo = Image.open("./Resources/thumbnail/reddit.png")
    
    draw = ImageDraw.Draw(img)
    
    #drawing episode text
    font = ImageFont.truetype("./Resources/OpenSans-Semibold.ttf", 300)
    w, h = draw.textsize("EP."+format(episode, '02'), font=font)

    draw.text(((1920-w)/2, (1080-h)/2-40),"EP."+format(episode, '02'),(0,0,0),font=font)
    draw.text(((1920-w)/2, (1080-h)/2-60),"EP."+format(episode, '02'),(255,255,255),font=font)

    #properties of episode text
    episode_top = (1080-h)/2-60
    episode_bottom = episode_top + h


    #drawing title text
    font_Small = ImageFont.truetype("./Resources/OpenSans-Semibold.ttf", 65)
    lines = textwrap.wrap(text, width=50)
    jointtext = "\n".join(lines)
    w2, h2 = draw.textsize(jointtext, font=font_Small)
    
    draw.text(((1920-w2)/2, episode_bottom+45),jointtext,(0,134,167),font=font_Small,align='center')
    draw.text(((1920-w2)/2,   episode_bottom+40),jointtext,(0,204,255),font=font_Small,align='center')

    #drawing AMAlogo
    logo_H = 173
    img.paste(AMAlogo,(415,int(episode_top-logo_H+70)),AMAlogo)

    #exporting
    img.save("thumbnail.png")

#textToImage("In grade 1 I had the 64 color crayola crayon box with the built in sharpener and the whole deal. One day after school, the guidance councilor needed some crayons and took my box telling my teacher he'd replace them. Three weeks later the fucking cocksucker gave me two 8 packs. I was devastated. AMA","0",0,"20")