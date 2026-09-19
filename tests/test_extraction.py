from unittest.mock import patch

from extraction.channel import get_channel
from extraction.videos import videos
from extraction.content import content



@patch("extraction.channel.videos")
@patch("extraction.channel.requests.get")
def test_channel(mock_get, mock_videos):

    mock_get.return_value.json.return_value = {
        "items": [
            {
                "id": "CHANNEL123",
                "contentDetails": {
                    "relatedPlaylists": {
                        "uploads": "UPLOADS123"
                    }
                }
            }
        ]
    }

    mock_videos.return_value = [
        {
            "videoId": "VIDEO001",
            "title": "Test Video"
        }
    ]

    result = get_channel("@mim-repository")

    assert result == [
        {
            "videoId": "VIDEO001",
            "title": "Test Video"
        }
    ]

    mock_videos.assert_called_once_with("UPLOADS123")


@patch("extraction.videos.content")
@patch("extraction.videos.requests.get")
def test_videos(mock_get, mock_content):

    mock_get.return_value.json.return_value = {
        "items": [
            {
                "snippet": {
                    "resourceId": {
                        "videoId": "VIDEO001"
                    }
                }
            }
        ],
        "nextPageToken": None
    }

    mock_content.return_value = [
        {
            "videoId": "VIDEO001",
            "title": "Test Video"
        }
    ]

    result = videos("UPLOADS123")

    assert len(result) == 1
    assert result[0]["videoId"] == "VIDEO001"
    assert result[0]["title"] == "Test Video"

    mock_content.assert_called_once_with(["VIDEO001"])




@patch("extraction.videos.content")
@patch("extraction.videos.requests.get")
def test_videos_pagination(mock_get, mock_content):

    mock_get.return_value.json.side_effect = [
        {
            "items": [
                {
                    "snippet": {
                        "resourceId": {
                            "videoId": "VIDEO001"
                        }
                    }
                }
            ],
            "nextPageToken": "TOKEN123"
        },
        {
            "items": [
                {
                    "snippet": {
                        "resourceId": {
                            "videoId": "VIDEO002"
                        }
                    }
                }
            ],
            "nextPageToken": None
        }
    ]

    mock_content.side_effect = [
        [
            {
                "videoId": "VIDEO001",
                "title": "Video 1"
            }
        ],
        [
            {
                "videoId": "VIDEO002",
                "title": "Video 2"
            }
        ]
    ]

    result = videos("UPLOADS123")

    assert len(result) == 2

    assert result[0]["videoId"] == "VIDEO001"
    assert result[1]["videoId"] == "VIDEO002"

    assert mock_get.call_count == 2
    assert mock_content.call_count == 2




@patch("extraction.content.requests.get")
def test_content(mock_get):

    mock_get.return_value.json.return_value = {
        "items": [
            {
                "id": "VIDEO001",

                "snippet": {
                    "title": "Test Video",
                    "publishedAt": "2026-09-17T10:00:00Z"
                },

                "contentDetails": {
                    "duration": "PT33S"
                },

                "statistics": {
                    "viewCount": "1000",
                    "likeCount": "50",
                    "commentCount": "10"
                }
            }
        ]
    }

    result = content(["VIDEO001"])

    assert len(result) == 1

    video = result[0]

    assert video["videoId"] == "VIDEO001"
    assert video["title"] == "Test Video"
    assert video["publishedAt"] == "2026-09-17T10:00:00Z"
    assert video["duration"] == "PT33S"
    assert video["viewCount"] == "1000"
    assert video["likeCount"] == "50"
    assert video["commentCount"] == "10"