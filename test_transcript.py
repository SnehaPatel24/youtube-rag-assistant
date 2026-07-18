from youtube_transcript_api import YouTubeTranscriptApi

video_id = "dQw4w9WgXcQ"  # Replace with any YouTube video ID

transcript = YouTubeTranscriptApi().fetch(video_id)

for item in transcript[:5]:
    print(item.text)