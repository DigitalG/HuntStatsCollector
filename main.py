import hashlib
import json
import time
import os

from packages.stats_collector.watcher import file_watcher
from packages.stats_collector.steampath import get_steam_library_path_for_game_id
from packages.stats_collector.parser import parse_hunt_xml_data
from packages.flask_app import create_app

steam_path = get_steam_library_path_for_game_id("594650")
xml_data_path = f"{steam_path}\\steamapps\\common\\Hunt Showdown\\user\\profiles\\default\\attributes.xml"
MATCHES_DATA_PATH = "data\\matches\\"

# Function that writes new JSON file if last entry is different from new file state
# Is called by watcher if filechange is detected
# TODO: Split in couple of functions
def write_parsed_data_in_json(xml_data_path):
    # This part is comparing hash from new data and last entry JSON data
    parsed_data = parse_hunt_xml_data(xml_data_path)
    parsed_string = json.dumps(parsed_data, sort_keys=True, indent=4).encode("utf-8")
    parsed_string_hashed = hashlib.md5(parsed_string).hexdigest()

    matches_data = os.listdir(MATCHES_DATA_PATH)
    if matches_data:
        with open(
            os.path.join(MATCHES_DATA_PATH, matches_data[-1]), "rb"
        ) as last_match_data:
            # FIXME: This monstrocity is the only way I could find to get rid of special chars and stuff, I hate it, needs fixing
            data_string = (
                last_match_data.read().decode("utf-8").replace("\r", "").encode("utf-8")
            )
        data_string_hashed = hashlib.md5(data_string).hexdigest()

        if data_string_hashed == parsed_string_hashed:
            print("Last hash is equal to new | No new entry added")
            return

    # Creating new JSOn file with parsed data. Name is generated from time since Epoch.
    with open(f"{MATCHES_DATA_PATH}{time.time_ns()}.json", "x") as f:
        f.write(json.dumps(parsed_data, indent=4, sort_keys=True))
    print("New match detected | New entry is added")

    return


def setup():
    try:
        os.makedirs(MATCHES_DATA_PATH)
    except OSError:
        print("Exsisting data folder found")

    (f"Output folder set up: {MATCHES_DATA_PATH}")


# Starting watcher here
if __name__ == "__main__":
    # setup()
    # file_watcher(xml_data_path, 10, write_parsed_data_in_json, xml_data_path)
    app = create_app(MATCHES_DATA_PATH, test_config=None)
    app.run(host="127.0.0.1", port=8000, debug=True)
