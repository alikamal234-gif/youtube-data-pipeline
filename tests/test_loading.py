from unittest.mock import patch, mock_open

from loading.postgres import staging_table_data




@patch("loading.postgres.connexion")
@patch("builtins.open", new_callable=mock_open)
@patch("loading.postgres.json.load")
def test_staging_table_data(mock_json_load, mock_open_file, mock_connexion ):


    mock_json_load.return_value = [
        {
            "videoId": "VIDEO001",
            "title": "Test Video",
            "publishedAt": "2026-09-17T10:00:00Z",
            "duration": "PT33S",
            "viewCount": 1000,
            "likeCount": 50,
            "commentCount": 10
        },
        {
            "videoId": "VIDEO002",
            "title": "Test Video 2",
            "publishedAt": "2026-09-17T11:00:00Z",
            "duration": "PT1M",
            "viewCount": 2000,
            "likeCount": 100,
            "commentCount": 20
        }
    ]

    mock_connection = mock_connexion.return_value
    mock_cursor = mock_connection.cursor.return_value

    mock_cursor.fetchall.return_value = [
        ("VIDEO001",),
        ("VIDEO002",)
    ]

    staging_table_data("data/test.json")

    mock_open_file.assert_called_once_with(
        "data/test.json",
        "r",
        encoding="utf-8"
    )

    mock_json_load.assert_called_once()

    mock_connexion.assert_called_once()
    assert mock_cursor.execute.call_count == 3
    mock_connection.commit.assert_called_once()

    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()