# RedditToYoutube
RedditToYoutube is a tool that automatically finds the most popular posts in the r/AMA subreddit and converts it to a high production animation that is uploaded to Youtube. The application uses Amazon's Polly service to convert text to speech and move.py and pillow python library create the animations, stitch together the audio and video and export the video.

## Usage
Add reddit and amazon polly API key to config.py.
Run `createAMAVideos(amount)` function from main.py where amount is the number of videos to create.
