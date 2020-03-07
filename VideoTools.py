from moviepy.editor import *
from moviepy.video.fx.all import loop, freeze
from TextToImage import textToImage
from TextToSpeech import textToSpeech
from texsplit import textsplit

img_OP = []
for x in range(0, 14):
    if x >9:
        img_OP.append("./Resources/OP_img/helo00"+str(x)+".png")
    else:
        img_OP.append("./Resources/OP_img/helo000"+str(x)+".png")

img_User = []
for x in range(0, 14):
    if x >9:
        img_User.append("./Resources/User_img/hel00"+str(x)+".png")
    else:
        img_User.append("./Resources/User_img/hel000"+str(x)+".png")

OP_img_sequence = ImageSequenceClip(img_OP, fps=24)
User_img_sequence = ImageSequenceClip(img_User, fps=24)


text = "A dramatic headline, I know, but my fuck has been a struggle to say the least. I‘m 32 now. In my early teens, my parents were in the process of a contentious and incredibly difficult separation when I was diagnosed with leukemia. They stayed together while I recovered, then completed their divorce as soon as I was in remission. The upheaval of all those years left me with anorexia, which has been a constant companion ever since. My leukemia came back in college and I came close to dying. Miraculously, I’m still here, but in the intervening years I’ve needed a kidney transplant, and anorexia is still something I live with. I’m on disability, have never finished college, and have never come close to building anything resembling a career. Quite a downer, right? Nevertheless, I have moments of happiness and contentment and I’m doing my best to have a life that means something to me despite my problems. Ask me anything."
def createClip(id,index,body):
    videoclips = []
    splitText = textsplit(body)
    iteration = 0
    last_iteration = len(splitText[0])-1

    for i in range(len(splitText[0])):
        fulltext = ""
        totaltext = "".join(splitText[0][i])
        for j in range(len(splitText[0][i])):
            video_clip = []
            phrase_img = splitText[0][i][j]
            phrase_polly = splitText[1][i][j]

            if phrase_img.strip() == "":
                continue
            fulltext = fulltext+phrase_img

            elipseTop = textToImage(fulltext, id, id=="1", str(index),str(iteration),totaltext)
            


            image_clip = ImageClip("./raw/"+str(index)+"/"+id+"_"+str(iteration)+".png")
            audio_clip = textToSpeech(phrase_polly, id, str(index),str(iteration))
            print(phrase_polly)
            video_clip = image_clip.set_duration(audio_clip.duration)
            if (id == "0"):
                img_sequence_loop = loop(User_img_sequence,duration=audio_clip.duration)
            else: 
                img_sequence_loop = loop(OP_img_sequence,duration=audio_clip.duration)

            #img_sequence_loop = freeze(img_sequence_loop, t="end",freeze_duration=0.5)
            img_sequence_loop = img_sequence_loop.set_position((744,elipseTop-77+23))
            video_clip = CompositeVideoClip([video_clip,img_sequence_loop])
            video_clip.audio = audio_clip

            videoclips.append(video_clip)
            iteration+=1

    #video_clip = freeze(video_clip,freeze_duration=0.5)
    final_clip = concatenate_videoclips(videoclips)

    #final_clip.write_videofile("output.mp4",fps=24)
    return final_clip

#print(textsplit(text))
