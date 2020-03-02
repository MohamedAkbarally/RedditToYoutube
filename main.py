import praw
from praw.models import MoreComments
import boto3
from TextToImage import textToImage
from TextToSpeech import textToSpeech
from VideoTools import createClip
from moviepy.editor import *
from moviepy.video.fx.all import loop


POSTS = 2
COMMENTS = 3

# textToSpeech("hello", "1")


reddit = praw.Reddit(client_id='OS91lmKHPbpU8Q',
                     client_secret='asuBtxV3YLUwQjhsX-a8_Jl13D8',
                     user_agent='my user agent')

subreddit = reddit.subreddit('AMA')

posts = []

for submission in subreddit.hot(limit=POSTS):
    post = {}
    post["id"] = submission.id
    post["author"] = submission.author.name
    post["over_18"] = submission.over_18
    post["title"] = submission.title
    post["description"] = submission.selftext
    posts.append(post)

posts = posts[1:]
print(posts)

comments = []
index = 0
clips = []

submission.comments.replace_more(limit=None)
for comment in submission.comments.list():
    if comment.is_submitter:
        question = reddit.comment(id=comment.parent_id[3:])
      
        clips.append(createClip("0",index,question.body))
        clips.append(createClip("1",index,comment.body))

        #textToImage(comment.body, "1", 1, str(index))
        #textToSpeech(comment.body, "1", str(index))
        #clips.append(createClip("1",0))
        #index +=1
        break 


final_clip = concatenate_videoclips(clips)
final_clip.write_videofile("flower.mp4",fps=24) # works !

