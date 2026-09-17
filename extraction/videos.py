import requests
import os
from dotenv import load_dotenv
from .content import content


def videos(playlist_id):

    load_dotenv()

    api_key = os.getenv("YOUTUBE_API_KEY")

    url = "https://www.googleapis.com/youtube/v3/playlistItems"

    all_items = []

    next_page_token = None

    while True:

        params = {
            "part": "snippet",
            "playlistId": playlist_id,
            "maxResults": 50,
            "key": api_key
        }

        if next_page_token:
            params["pageToken"] = next_page_token

        response = requests.get(url=url, params=params)
        data = response.json()

        video_ids = []

        for item in data.get("items", []):
            video_id = item["snippet"]["resourceId"]["videoId"]
            video_ids.append(video_id)

        if video_ids:
            batch_data = content(video_ids)
            all_items.extend(batch_data)

        next_page_token = data.get("nextPageToken")

        if not next_page_token:
            break

    return all_items