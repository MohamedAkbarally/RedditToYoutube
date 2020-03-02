import boto3
import os


def textToSpeech(text, id, folder):
    polly = boto3.client('polly')
    if id == "0":
        spoken_text = polly.synthesize_speech(Text=text,
                                          OutputFormat='mp3',
                                          VoiceId='Joanna')
    else:
        spoken_text = polly.synthesize_speech(Text=text,
                                          OutputFormat='mp3',
                                          VoiceId='Salli')


    filename = "./raw/"+folder+"/"+id+".mp3"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'wb') as f:
        f.write(spoken_text['AudioStream'].read())
        f.close()
