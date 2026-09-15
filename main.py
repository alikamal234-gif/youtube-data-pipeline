from extraction.extraction import extraction
import json


data = extraction("@mim-repository")
# print(data)
with open("data/YT_data_2026-09-14.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("JSON enregistré avec succès !")