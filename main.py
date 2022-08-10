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


file_watcher(xml_data_path, 1, write_parsed_data_in_json, xml_data_path)
