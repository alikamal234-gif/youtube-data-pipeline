import requests
import os
from dotenv import load_dotenv
import sys


def content(video_ids):
    load_dotenv()

    api_key = os.getenv("YOUTUBE_API_KEY")

    url = "https://www.googleapis.com/youtube/v3/videos"

    params = {
        "part": "snippet,contentDetails,statistics",
        "id": ",".join(video_ids),
        "key": api_key
    }

    response = requests.get(url=url, params=params)
    data = response.json()

    videos = []

    for item in data.get("items", []):

        video = {
            "videoId": item["id"],
            "title": item["snippet"]["title"],
            "publishedAt": item["snippet"]["publishedAt"],
            "duration": item["contentDetails"]["duration"],
            "viewCount": item["statistics"].get("viewCount"),
            "likeCount": item["statistics"].get("likeCount"),
            "commentCount": item["statistics"].get("commentCount")
        }

        videos.append(video)

    return videos