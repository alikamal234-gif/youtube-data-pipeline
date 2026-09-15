import os
import requests
from dotenv import load_dotenv
from .videos import videos


def get_channel(forHandle):

    load_dotenv()

    api_key = os.getenv("YOUTUBE_API_KEY")

    url = "https://www.googleapis.com/youtube/v3/channels"

    params = {
        "part": "id,contentDetails",
        "forHandle": forHandle,
        "key": api_key
    }

    response = requests.get(url=url, params=params)

    data = response.json()


    uploads_playlist_id = data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    return videos(uploads_playlist_id)