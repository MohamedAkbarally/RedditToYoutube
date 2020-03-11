from PIL import Image, ImageFont, ImageDraw
import textwrap
import os
from moviepy.editor import *


def textToImage(text, isOP, folder,part,textfull):
    """saves an image in raw folder with text
        returns the top of the card within the image

        Parameters
        ----------
        text : str
            the text to be displayed in the image

        isOP : boolean
            0 is a user comment, 1 is an OP comment
        
        folder : str
            the folder the image will be stored
        
        part : str
            the part in the img sequence

        textfull : str
            the entire text to be displayed in the the current page
    """

    font = ImageFont.truetype("./Resources/OpenSans.ttf", 55)

    #selects the background of the image
    if isOP:
        img = Image.open("./Resources/backgrouda.png")
    else:
        img = Image.open("./Resources/backgroudq.png")
    
    #canvas
    draw = ImageDraw.Draw(img)

    #wraps text to fit in 50 character lines
    lines = textwrap.wrap(text, width=50)
    wrapped_text = "\n".join(lines)

    #gets dimensions of text in the entire page
    linesfull = textwrap.wrap(textfull, width=50)
    wraped_textfull = "\n".join(linesfull)
    textfull_width, textfull_height = draw.textsize(wraped_textfull, font=font)

    #textfull_minwidth stores minimum width of card (used to diplay text within)
    textfull_minwidth = textfull_width
    if textfull_width < 1020:
        textfull_minwidth = 1020

    #card properties
    card_top = (1080-textfull_height)/2
    card_left = (1920-textfull_minwidth)/2
    card_bottom = card_top+textfull_height
    card_right = card_left+textfull_minwidth 

    #elipse properties
    elipseH =111*2
    elipse_offset = elipseH/4
    eslipseW = 290
    elipse_top = ((1080-elipseH)/2) - (textfull_height+200)/2
    elipse_left = (1920-eslipseW)/2
    elipse_bottom = elipse_top+elipseH
    elipse_right =  elipse_left+eslipseW

    #drawing eclipse shadow
    shape_shadow = [(elipse_left, elipse_top+elipse_offset),
             (elipse_right+9,elipse_bottom+elipse_offset)]
    draw.ellipse(shape_shadow, fill="#383838")

    #drawing eclipse
    shape = [(elipse_left, elipse_top+elipse_offset),
             (elipse_right,elipse_bottom+elipse_offset)]
    draw.ellipse(shape, fill="#000000")

    #drawing card shadow
    shape = [(card_left-100, card_top-110+elipse_offset), 
             (card_right+100+9,card_bottom+72+9+elipse_offset)]
    draw.rectangle(shape, fill="#383838")

    #drawing card
    shape = [(card_left-100, card_top-110+elipse_offset), 
             (card_right+100, card_bottom+72+elipse_offset)]
    draw.rectangle(shape, fill="#000000")

    #drawing text
    draw.text(((1920-textfull_width)/2, (1080-textfull_height)/2+elipse_offset), wrapped_text, font=font, fill="white",align='left')

    #exporting image
    filename = "./raw/"+folder+"/"+str(isOP)+"_"+part+".png"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save(filename)
    
    #returning top of image
    return elipse_top+elipse_offset


def createAMAThumbnail(text, episode):
    """saves an image in output folder of the thumbnail for the relavant episode

        Parameters
        ----------
        text : str
            the text to be displayed in the image

        episode : int
           the episode number of the video
    """
    #trimming text to the last word below 100 characters
    if len(text)> 100:
        text = text[:100].rsplit(' ', 1)[0] + "..."
    
    img = Image.open("./Resources/thumbnail/bg.png")
    AMAlogo = Image.open("./Resources/thumbnail/reddit.png")
    episodeFont = ImageFont.truetype("./Resources/OpenSans-Semibold.ttf", 180)
    titleFont = ImageFont.truetype("./Resources/OpenSans-Semibold.ttf", 120)
    
    #canvas
    draw = ImageDraw.Draw(img)
    
    #drawing title text
    lines = textwrap.wrap(text, width=28)
    jointtext = "\n".join(lines)

    #draw title text and shadow
    titleText_width, titleText_height = draw.textsize(jointtext, font=titleFont)
    draw.text(((1920-titleText_width)/2, (1080-titleText_height)/2-0),jointtext,(0,134,167),font=titleFont,align='center')
    draw.text(((1920-titleText_width)/2, (1080-titleText_height)/2-8),jointtext,(0,204,255),font=titleFont,align='center')

    #properties of title text
    episode_top = (1080-titleText_height)/2-60
    episode_bottom = episode_top + titleText_height

    #drawing epside text
    episodeText_width, episodeText_height = draw.textsize("EP."+format(episode, '02'), font=episodeFont)
    draw.text(((1920-episodeText_width)/2, episode_bottom+75),"EP."+format(episode, '02'),(0,0,0),font=episodeFont,align='center')
    draw.text(((1920-episodeText_width)/2,   episode_bottom+60),"EP."+format(episode, '02'),(255,255,255),font=episodeFont,align='center')

    #drawing AMAlogo
    logo_H = 173
    img.paste(AMAlogo,(415,int(episode_top-logo_H+50)),AMAlogo)

    #exporting thumbnail
    os.makedirs(os.path.dirname("./output/"+str(episode)+"/thumbnail.png"), exist_ok=True)
    img.save("./output/"+str(episode)+"/thumbnail.png")

