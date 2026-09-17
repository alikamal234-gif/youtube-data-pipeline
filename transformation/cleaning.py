from loading.connexion import connexion 
import pandas as pd


def cleaning():
    conn  = connexion()

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM staging.videos")
    videos = cursor.fetchall() 
    data = pd.DataFrame(videos , columns=[
        "video_id",
        "title",
        "published_at",
        "duration",
        "views",
        "likes",
        "comments"
    ])
    data["published_at"] = pd.to_datetime(data["published_at"])
    data["views"] = pd.to_numeric(data["views"] , errors="coerce")
    data["likes"] = pd.to_numeric(data["likes"] , errors="coerce")
    data["comments"] = pd.to_numeric(data["comments"] , errors="coerce")



    def duration_format(durations):
        new_durations = []
        for duration in durations:
            time_unite = ["H" , "M" , "S"]
            time = ""
            target = duration[2:]
            time_final = 0
            for dur in target:
                if dur in time_unite:
                    if dur == "H":
                        time_final += int(time) * 3600
                    elif dur == "M" :
                        time_final += int(time) * 60
                    elif dur == "S" :
                        time_final += int(time)
                    time = ""
                else :
                    time += dur
            new_durations.append(time_final)
        return pd.Series(new_durations) 


    data["duration"] = duration_format(data["duration"])
    if data["video_id"].duplicated().sum() > 0 :
        data = data.drop_duplicates(subset="video_id")
    print(data["video_id"].duplicated().sum())
    print(data.head())
    print(data.dtypes)
    print(data.isnull().sum())

    return data


