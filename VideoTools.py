from moviepy.editor import *
from moviepy.video.fx.all import loop, freeze
from TextToImage import textToImage
from TextToSpeech import textToSpeech

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


def createClip(id,index,body):
    elipseTop = textToImage(body, id, id=="1", str(index))
    textToSpeech(body, id, str(index))

    image_clip = ImageClip("./raw/"+str(index)+"/"+id+".png")
    audio_clip = AudioFileClip("./raw/"+str(index)+"/"+id+".mp3")
    video_clip = image_clip.set_duration(audio_clip.duration + 0.5)
    if (id == 0):
        img_sequence_loop = loop(User_img_sequence,duration=audio_clip.duration)
    else: 
        img_sequence_loop = loop(OP_img_sequence,duration=audio_clip.duration)

    img_sequence_loop = freeze(img_sequence_loop, t="end",freeze_duration=0.5)
    img_sequence_loop = img_sequence_loop.set_position((744,elipseTop-77+23))
    video_clip = CompositeVideoClip([video_clip,img_sequence_loop])
    video_clip.audio = audio_clip
    video_clip = freeze(video_clip,freeze_duration=0.5)
    return video_clip