# RedditToYoutube
RedditToYoutube is a tool that automatically finds the most popular posts in the r/AMA subreddit and converts them to a high production animation that is uploaded to Youtube. The application uses Amazon's Polly service to convert text to speech, and move.py and pillow to create the animations. The video is then programmatically stitched together with audio and video and exported.

## Usage
Add reddit and amazon polly API key to config.py.
Run `createAMAVideos(amount)` function from main.py where amount is the number of videos to create.
