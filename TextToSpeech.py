import boto3
import os
from moviepy.editor import *

def textToSpeech(text, isOP, folder, part):
    """return a audio clip object of the text with censoring of explitives

        Parameters
        ----------
        text : str
            the text to be spoken

        isOP : boolean
            0 is a user comment, 1 is an OP comment
        
        folder : str
            the folder the image will be stored
        
        part : str
            the part in the audio sequence
    """
    polly = boto3.client('polly')
    print(text)
    #selecting voice
    speaker = "Salli"
    if not isOP:
        speaker = "Joanna"

    censorbeep = AudioFileClip("./Resources/censor_beep.mp3")

    #splitting clips based on explitive
    textarray = text.split("</beep>")

    clips = []
    index = 0
    
    for splitPart in textarray:
        if splitPart =="":
            clips.append(censorbeep)
            continue

        spoken_text = polly.synthesize_speech(Text=splitPart,
                                            OutputFormat='mp3',
                                            VoiceId=speaker)


        #storing raw audio files
        filename = "./raw/"+folder+"/"+str(isOP)+"_"+part+"_"+str(index)+".mp3"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as f:
            f.write(spoken_text['AudioStream'].read())
            f.close()

        clips.append(AudioFileClip(filename))
        clips.append(censorbeep)
        index+=1
        
    clips.pop()

    #concatenating audio clips
    final_clip = concatenate_audioclips(clips)
    return final_clip
   