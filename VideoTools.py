from moviepy.editor import *
from moviepy.video.fx.all import loop, freeze
from TextToImage import textToImage
from TextToSpeech import textToSpeech
from texsplit import textsplit
from PIL import Image, ImageFont, ImageDraw
import boto3

#image sequence for OP talking animation
img_OP = []
for x in range(0, 14):
    if x >9:
        img_OP.append("./Resources/OP_img/helo00"+str(x)+".png")
    else:
        img_OP.append("./Resources/OP_img/helo000"+str(x)+".png")

#image sequence for User talking animation
img_User = []
for x in range(0, 14):
    if x >9:
        img_User.append("./Resources/User_img/hel00"+str(x)+".png")
    else:
        img_User.append("./Resources/User_img/hel000"+str(x)+".png")

OP_img_sequence = ImageSequenceClip(img_OP, fps=24)
User_img_sequence = ImageSequenceClip(img_User, fps=24)

def createTextClip(isOP,comment_no,body):
    """returns a videoclip object for either a question or an answer

        Parameters
        ----------
        isOP : boolean
            0 is a user comment, 1 is an OP comment
        
        comment_no : int
            reference to which folder to store raw assets
        
        body : str
            the text to be displayed in the video clip
    """
    videoclips = []

    #splits texts into pages and segments
    splitText = textsplit(body)

    iteration = 0
    for i in range(len(splitText[0])):

        #full text stores the entire text to be displayed on the screen
        fulltext = ""
        
        #totaltext stores the entire text stored on one page
        totaltext = "".join(splitText[0][i])
        
        for j in range(len(splitText[0][i])):
            video_clip = []
            phrase_img = splitText[0][i][j]
            phrase_polly = splitText[1][i][j]

            #check if the phrase is blank
            if phrase_img.strip() == "":
                continue
            
            fulltext = fulltext+phrase_img
            
            #create image for text
            imageTop = textToImage(fulltext, isOP, str(comment_no),str(iteration),totaltext)

            #loads image created
            image_clip = ImageClip("./raw/"+str(comment_no)+"/"+str(isOP)+"_"+str(iteration)+".png")
            
            #creates audio clips for text
            audio_clip = textToSpeech(phrase_polly, isOP, str(comment_no),str(iteration))
            video_clip = image_clip.set_duration(audio_clip.duration)

            #adds talking head to video clip
            if not isOP:
                img_sequence_loop = loop(User_img_sequence,duration=audio_clip.duration)
            else: 
                img_sequence_loop = loop(OP_img_sequence,duration=audio_clip.duration)
            img_sequence_loop = img_sequence_loop.set_position((744,imageTop-77+23))
            video_clip = CompositeVideoClip([video_clip,img_sequence_loop])

            #adds audio to video clip
            video_clip.audio = audio_clip

            videoclips.append(video_clip)
            iteration+=1


    final_clip = concatenate_videoclips(videoclips)
    return final_clip

def createTitle(episode):
    """returns a video clip object of the intro to the relavant episode

        Parameters
        ----------
        episode : int
            the episode number of the video

    """
    img = Image.open("./Resources/backgrouda.png")
    font = ImageFont.truetype("./Resources/OpenSans-Semibold.ttf", 300)    
    
    #canvas
    draw = ImageDraw.Draw(img)

    w, h = draw.textsize("EP."+format(episode, '02'), font=font)

    #draw episode text and shadow
    draw.text(((1920-w)/2, (1080-h)/2-40),"EP."+format(episode, '02'),(0,0,0),font=font,align='center')
    draw.text(((1920-w)/2, (1080-h)/2-48),"EP."+format(episode, '02'),(255,355,255),font=font,align='center')
    
    #save image
    filename = "./raw/title/title.png"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save(filename)

    #save audio for intro
    polly = boto3.client('polly')
    spoken_text = polly.synthesize_speech(Text="<speak><break time=\"0.5s\"/><prosody rate=\"slow\">Reddit Ask Me Anything, Episode "+str(episode)+"</prosody><break time=\"0.2s\"/></speak>",
                                            OutputFormat='mp3',
                                            VoiceId="Salli", TextType='ssml')

    filename = "./raw/title/title.mp3"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(spoken_text['AudioStream'].read())
        f.close()

    #contructing videoclip object
    image_clip = ImageClip("./raw/title/title.png")
    audio_clip = AudioFileClip("./raw/title/title.mp3")
    video_clip = image_clip.set_duration(audio_clip.duration)
    video_clip.audio = audio_clip

    return video_clip
