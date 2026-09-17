from .connexion import connexion
import json
from transformation.cleaning import cleaning



# connection = connexion()
# cursor = connection.cursor()


def staging_table_data(path):
    connection = connexion()
    cursor = connection.cursor()
    with open(path, "r", encoding="utf-8") as f:
        videos = json.load(f)

    query = """
INSERT INTO staging.videos
(video_id, title, published_at, duration, views, likes, comments)
VALUES (%s, %s, %s, %s, %s, %s, %s)

ON CONFLICT (video_id)
DO UPDATE SET
    title = EXCLUDED.title,
    published_at = EXCLUDED.published_at,
    duration = EXCLUDED.duration,
    views = EXCLUDED.views,
    likes = EXCLUDED.likes,
    comments = EXCLUDED.comments
    """

    for video in videos:
        cursor.execute(
            query,
            (
                video["videoId"],
                video["title"],
                video["publishedAt"],
                video["duration"],
                video["viewCount"],
                video["likeCount"],
                video["commentCount"]
            )
        )

    new_video_ids = {
        video["videoId"]
        for video in videos
    }
    
    cursor.execute("SELECT video_id FROM staging.videos")

    existing_video_ids = {
        row[0]
        for row in cursor.fetchall()
    }

    ids_to_delete = existing_video_ids - new_video_ids

    for video_id in ids_to_delete:

        cursor.execute(
            "DELETE FROM staging.videos WHERE video_id = %s",
            (video_id,)
        )
    connection.commit()
    cursor.close()
    connection.close()
    print("Données insérées avec succès !")

def core_table_data():
    connection = connexion()
    cursor = connection.cursor()
    videos = cleaning()

    query = """
    INSERT INTO core.videos
    (video_id, title, published_at, duration_seconds, views, likes, comments)
    VALUES (%s, %s, %s, %s, %s, %s, %s)

    ON CONFLICT (video_id)
    DO UPDATE SET
        title = EXCLUDED.title,
        published_at = EXCLUDED.published_at,
        duration_seconds = EXCLUDED.duration_seconds,
        views = EXCLUDED.views,
        likes = EXCLUDED.likes,
        comments = EXCLUDED.comments
    """

    for _, video in videos.iterrows():

        cursor.execute(
            query,
            (
                video["video_id"],
                video["title"],
                video["published_at"],
                video["duration"],
                video["views"],
                video["likes"],
                video["comments"]
            )
        )
    new_video_ids = set(videos["video_id"])

    cursor.execute("SELECT video_id FROM core.videos")

    existing_video_ids = {
        row[0]
        for row in cursor.fetchall()
    }

    ids_to_delete = existing_video_ids - new_video_ids

    for video_id in ids_to_delete:

        cursor.execute(
            "DELETE FROM core.videos WHERE video_id = %s",
            (video_id,)
        )
    connection.commit()

    print("Données nettoyées insérées dans core !")

    cursor.close()
    connection.close()