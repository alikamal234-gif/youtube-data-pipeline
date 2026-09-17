from extraction.extraction import extraction
from transformation.cleaning import cleaning
from loading.postgres import core_table_data , staging_table_data
import json

path = "c:/Users/Youcode/Desktop/youtube-data-pipeline/data/YT_data_2026-09-14.json"
data = extraction("@mim-repository")
with open("data/YT_data_2026-09-14.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

staging_table_data(path)
core_table_data()
