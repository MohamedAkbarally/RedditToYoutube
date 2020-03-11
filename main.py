import praw
from praw.models import MoreComments
from moviepy.editor import *
from moviepy.video.fx.all import loop
from config import client_id, client_secret
from TextToImage import textToImage, createAMAThumbnail
from TextToSpeech import textToSpeech
from VideoTools import createTextClip, createTitle
import sys
import pickle


#import reddit API keys from config.py
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent='my user agent')

def createAMAVideos(amount):
    """saves an videos in the output folder of reddit AMA submissions

        Parameters
        ----------
        amount : int
            the amount of videos the user wants the program to produce
    """
    #maximum number of videos in one execution
    MAX_POST_NO = 30

    #maximum number of comments used to make a video
    MAX_COMMENT_NO = 1

    #minimum number of comments by owner required to make a video
    MIN_COMMENT_NO = 0

    subreddit = reddit.subreddit('AMA')

    #load episode number
    file1 = open("episode.txt","r") 
    episode = int(file1.read())
    file1.close()

    #load list of posts already done
    file1 = open("doneList.txt","r") 
    doneList = file1.readlines()
    file1.close() 

    #load backgroud audio
    BGaudio = AudioFileClip("./Resources/Sleeplessness.mp3")

    #load transition clip
    beep = VideoFileClip("./Resources/beep.m4v")

    #load outro clip
    outro = VideoFileClip("./Resources/outro.m4v")

    videos_made = 0

    #loop through submissions
    for submission in subreddit.top(limit=MAX_POST_NO):
        print("Making Episode "+str(episode))
        
        doneList.append(submission.id)

        #add submission to list
        with open('doneList.txt', 'wb') as fp:
            pickle.dump(doneList, fp)

        #verify submission is under 18 content
        if submission.over_18 == True:
                continue

        #verify submission has not already been used for a video
        if submission.id+"\n" in doneList:
            continue

        #Creates the appropriate thumbnail for the video
        createAMAThumbnail(submission.title,episode)

        #Array of all clips that form the video
        clips = []

        #AMA title
        clips.append(createTitle(episode))
        clips.append(createTextClip("1",-1,submission.title.replace('\n', ' ').replace('\r', '')))
        
        #AMA description
        if submission.selftext:
            clips.append(createTextClip("1",-2,submission.selftext.replace('\n', ' ').replace('\r', '')))

        clips.append(beep)

        
        comment_no = 0
        submission.comments.replace_more(limit=None)

        #loop through all comments
        for comment in submission.comments.list():
            if not comment.is_submitter:
                continue
            if not comment.parent_id:
                continue
            if not comment.body:
                continue
            

            question = reddit.comment(id=comment.parent_id[3:])

            if question.is_submitter:
                continue

            qtext = question.body.replace('\n', ' ')
            ctext = comment.body.replace('\n', ' ')

            #create question clip
            clips.append(createTextClip(0,comment_no,qtext))

            #create answer clip
            clips.append(createTextClip(1,comment_no,ctext))

            #add transition clip
            clips.append(beep)
            
            comment_no+=1
            if comment_no == MAX_COMMENT_NO:
                break
        
        if comment_no < MIN_COMMENT_NO:
            continue
        
        print("Raw files created")

        #concatenate all clips in clips array      
        final_clip = concatenate_videoclips(clips)

        #add BGaudio to final clip
        new_audioclip = CompositeAudioClip([final_clip.audio, BGaudio])
        new_audioclip = new_audioclip.set_duration(final_clip.duration)
        final_clip.audio = new_audioclip

        #add outro clip
        final_clip = concatenate_videoclips([final_clip,outro])

        #export final clip
        print("Exporting Episode "+str(episode))
        os.makedirs(os.path.dirname("./output/"+str(episode)+"/output.mp4"), exist_ok=True)
        final_clip.write_videofile("./output/"+str(episode)+"/output.mp4",fps=24)

        for clip in clips:
            clip.close()
            
        final_clip.close()
        new_audioclip.close()

        #increment episode number
        file1 = open("episode.txt","w")#write mode
        episode +=1
        file1.write(str(episode))
        file1.close()

        videos_made += 1
        if videos_made == amount:
            print("Done")
            return


createAMAVideos(1)

