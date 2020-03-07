import boto3
import os
from moviepy.editor import *

#converts text to speech file
def textToSpeech(text, name, folder, part):
    polly = boto3.client('polly')
    print("speaking"+text)

    textarray = text.split("</beep>")
    speaker = ""
    #selecting voice
    if name == "0":
        speaker = "Joanna"
    else:
        speaker = "Salli"
    
    index = 0
    clips = []

    censorbeep = AudioFileClip("./Resources/censor_beep.mp3")

    for splitPart in textarray:
        if splitPart =="":
            clips.append(censorbeep)
            continue


        spoken_text = polly.synthesize_speech(Text=splitPart,
                                            OutputFormat='mp3',
                                            VoiceId=speaker)


        #storing file
        filename = "./raw/"+folder+"/"+name+"_"+part+"_"+str(index)+".mp3"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as f:
            f.write(spoken_text['AudioStream'].read())
            f.close()
        clips.append(AudioFileClip(filename))
        clips.append(censorbeep)
        index+=1
        
    clips.pop()
    final_clip = concatenate_audioclips(clips)
    return final_clip
   