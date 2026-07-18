from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from urllib.parse import urlparse, parse_qs


def extract_video_id(url):

    if "youtu.be" in url:
        return url.split("/")[-1]

    parsed = urlparse(url)

    if parsed.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed.query)["v"][0]

    return url


def get_transcript(url):

    video_id = extract_video_id(url)

    try:
        yt = YouTubeTranscriptApi()

        transcript = yt.fetch(video_id)

        text = " ".join(chunk.text for chunk in transcript)

        return text

    except TranscriptsDisabled:
        return None

    except Exception as e:
        print(e)
        return None