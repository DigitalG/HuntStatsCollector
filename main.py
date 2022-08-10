import json
import os
import time

from watcher import file_watcher
from steampath import get_steam_library_path_for_game_id
from parser import parse_hunt_xml_data

steam_path = get_steam_library_path_for_game_id("594650")
xml_data_path = f"{steam_path}\\steamapps\\common\\Hunt Showdown\\user\\profiles\\default\\attributes.xml"

OUTPUT_PATH = "data\\matches\\"


def write_parsed_data_in_json(xml_data_path):
    with open(f"{OUTPUT_PATH}{time.time_ns()}.json", "x") as f:
        f.write(
            json.dumps(parse_hunt_xml_data(xml_data_path), indent=4, sort_keys=True)
        )
    return


# for entry_num in sorted(mission_teams_dict.keys()):
#     print(f"{entry_num} ---")
#     for key, value in mission_teams_dict[entry_num].items():
#         print(f"\t{key} : {value}")
# долбайоб насрав закоментованого в мейн бренчу сука блять "ой а нахуя нам ото блять пуш в мастер сука"
# (мідл кстате 2.5 зпшка)
# він може коменти потім видалити но тіпа ця історія збережеться
print(json.dumps(mission_teams_dict, sort_keys=True, indent=4))

# якшо даня прочитав це то він ебать лох пізда