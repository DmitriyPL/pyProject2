import pprint
import json

import data


data_for_write = {'goals': data.goals, 'teachers': data.teachers}

with open("databaseJSON.json", "w", encoding="utf-8") as databaseJSON:
    json.dump(data_for_write, databaseJSON)

# Проверка записи!
#
# with open("databaseJSON.json", "r", encoding="utf-8") as databaseJSON:
#     contents = json.load(databaseJSON)
#
# pprint.pprint(contents)