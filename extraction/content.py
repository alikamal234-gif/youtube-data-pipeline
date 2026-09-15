import requests
import os
from dotenv import load_dotenv
import sys


def content(video_ids):

    load_dotenv()
    sys.stdout.reconfigure(encoding="utf-8")

    api_key = os.getenv("YOUTUBE_API_KEY")
    url = "https://www.googleapis.com/youtube/v3/videos"

    params = {
        "part": "snippet,contentDetails,statistics",
        "id": ",".join(video_ids),
        "key": api_key
    }

    response = requests.get(url=url, params=params)

    data = response.json()

    return data.get("items", [])