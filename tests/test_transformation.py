from unittest.mock import patch
import pandas as pd
from transformation.cleaning import cleaning

@patch("transformation.cleaning.connexion")
def test_cleaning(mock_connexion):

    mock_connection = mock_connexion.return_value
    mock_cursor = mock_connection.cursor.return_value

    mock_cursor.fetchall.return_value = [
        (
            "VIDEO001",
            "Test Video",
            "2026-09-17T10:00:00Z",
            "PT33S",
            "1000",
            "50",
            "10"
        ),
        (
            "VIDEO002",
            "Test Video 2",
            "2026-09-17T11:00:00Z",
            "PT1M30S",
            "2000",
            "100",
            "20"
        )
    ]

    result = cleaning()

    assert isinstance(result, pd.DataFrame)

    assert len(result) == 2

    assert list(result.columns) == [
        "video_id",
        "title",
        "published_at",
        "duration",
        "views",
        "likes",
        "comments"
    ]

    assert result.loc[0, "duration"] == 33
    assert result.loc[1, "duration"] == 90

    assert result["views"].dtype.kind in "iu"
    assert result["likes"].dtype.kind in "iu"
    assert result["comments"].dtype.kind in "iu"

    assert pd.api.types.is_datetime64_any_dtype(
        result["published_at"]
    )

    assert result["video_id"].duplicated().sum() == 0

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM staging.videos"
    )