import praw
from praw.models import MoreComments
import boto3
from TextToImage import textToImage, AMAThumbnail
from TextToSpeech import textToSpeech
from VideoTools import createClip
from moviepy.editor import *
from moviepy.video.fx.all import loop

#Number of the post
POST_NO = 2

reddit = praw.Reddit(client_id='OS91lmKHPbpU8Q',
                     client_secret='asuBtxV3YLUwQjhsX-a8_Jl13D8',
                     user_agent='my user agent')

subreddit = reddit.subreddit('AMA')

posts = []

#loop through submissions
for submission in subreddit.hot(limit=POST_NO):
    post = {}
    post["id"] = submission.id
    #post["author"] = submission.author.name
    post["over_18"] = submission.over_18
    post["title"] = submission.title
    post["description"] = submission.selftext
    submission.comments.replace_more(limit=None)
    post["comments"] = submission.comments.list()
    posts.append(post)


#create thumnail
AMAThumbnail(posts[0]["title"],1)


BGaudio = AudioFileClip("./Resources/Sleeplessness.mp3")


#transition beep clip
beep = VideoFileClip("./Resources/beep.m4v")

#outro clip
outro = VideoFileClip("./Resources/outro.m4v")

#store of all the clips that form the video 
clips = []

clips.append(createClip("1",-1,posts[0]["title"].replace('\n', ' ').replace('\r', '')))
if post["description"]:
    clips.append(createClip("1",-2,posts[0]["description"].replace('\n', ' ').replace('\r', '')))

clips.append(beep)


comments = []
index = 0

#loop through all comments
for comment in posts[0]["comments"]:
    if comment.is_submitter:
        question = reddit.comment(id=comment.parent_id[3:])
        print("yello")
        qtext = question.body.replace('\n', ' ').replace('\r', '')
        ctext = comment.body.replace('\n', ' ').replace('\r', '')

        #create question clip
        clips.append(createClip("0",index,qtext))

        #create answer clip
        clips.append(createClip("1",index,ctext))

        clips.append(beep)

        break
        
final_clip = concatenate_videoclips(clips)
new_audioclip = CompositeAudioClip([final_clip.audio, BGaudio])
new_audioclip = new_audioclip.set_duration(final_clip.duration)
final_clip.audio = new_audioclip
#clips.append(outro)
final_clip = concatenate_videoclips([final_clip,outro])
#exporting
final_clip.write_videofile("output.mp4",fps=24)

