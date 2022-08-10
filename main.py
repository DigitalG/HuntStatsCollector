import json
from lxml import etree

from steampath import get_steam_library_path_for_game_id


steam_path = get_steam_library_path_for_game_id("594650")
xml_data_path = f"{steam_path}\\steamapps\\common\\Hunt Showdown\\user\\profiles\\default\\attributes.xml"
with open(xml_data_path, "r", encoding="UTF-8") as f:
    xml_data = f.read()
root = etree.fromstring(xml_data)
mission = [element for element in root if element.get("name").startswith("Mission")]
mission_entried = [
    element for element in root if element.get("name").startswith("MissionBagEntry")
]
mission_accolade_entried = [
    element
    for element in root
    if element.get("name").startswith("MissionAccoladeEntry")
]
mission_players = [
    element for element in root if element.get("name").startswith("MissionBagPlayer")
]
mission_teams = [
    element for element in root if element.get("name").startswith("MissionBagTeam")
]

number_of_teams = [
    element for element in root if element.get("name").startswith("MissionBagNumTeams")
][0].get("value")
number_of_entries = [
    element
    for element in root
    if element.get("name").startswith("MissionBagNumEntries")
][0].get("value")
number_of_accolades = [
    element
    for element in root
    if element.get("name").startswith("MissionBagNumEntries")
][0].get("value")


mission_bag_entry_dict = {}

for entry in mission_entried:
    entry_name_split = entry.get("name").split("_")
    # ignore useless entries
    if len(entry_name_split) < 3:
        continue
    entry_number = int(entry_name_split[1])
    if entry_number > int(number_of_entries) - 1:
        continue
    entry_attribute_name = entry_name_split[2]
    if entry_number not in mission_bag_entry_dict.keys():
        mission_bag_entry_dict[entry_number] = {}
    mission_bag_entry_dict[entry_number][entry_attribute_name] = entry.get("value")

mission_bag_accolade_entry_dict = {}

for entry in mission_accolade_entried:
    entry_name_split = entry.get("name").split("_")
    # ignore useless entries
    if len(entry_name_split) < 3:
        continue
    entry_number = int(entry_name_split[1])
    if entry_number > int(number_of_accolades) - 1:
        continue
    entry_attribute_name = entry_name_split[2]
    if entry_number not in mission_bag_accolade_entry_dict.keys():
        mission_bag_accolade_entry_dict[entry_number] = {}
    mission_bag_accolade_entry_dict[entry_number][entry_attribute_name] = entry.get(
        "value"
    )

mission_teams_dict = {}

for entry in mission_teams:
    entry_name_split = entry.get("name").split("_")
    if len(entry_name_split) < 3:
        continue
    team_number = int(entry_name_split[1])
    if team_number > int(number_of_teams) - 1:
        continue
    team_attribute_name = entry_name_split[2]
    if team_number not in mission_teams_dict.keys():
        mission_teams_dict[team_number] = {}
    mission_teams_dict[team_number][team_attribute_name] = entry.get("value")


for entry in mission_players:
    entry_name_split = entry.get("name").split("_")
    if len(entry_name_split) < 4:
        continue
    team_number = int(entry_name_split[1])
    if team_number > int(number_of_teams) - 1:
        continue
    player_number = int(entry_name_split[2])
    if player_number > int(mission_teams_dict[team_number]["numplayers"]) - 1:
        continue
    player_attribute_name = entry_name_split[3]

    if "players" not in mission_teams_dict[team_number].keys():
        mission_teams_dict[team_number]["players"] = {}
    if player_number not in mission_teams_dict[team_number]["players"].keys():
        mission_teams_dict[team_number]["players"][player_number] = {}
    mission_teams_dict[team_number]["players"][player_number][
        player_attribute_name
    ] = entry.get("value")


# for entry_num in sorted(mission_bag_entry_dict.keys()):
#     print(f"{entry_num} ---")
#     for key, value in mission_bag_entry_dict[entry_num].items():
#         print(f"\t{key} : {value}")

# for entry_num in sorted(mission_bag_accolade_entry_dict.keys()):
#     print(f"{entry_num} ---")
#     for key, value in mission_bag_entry_dict[entry_num].items():
#         print(f"\t{key} : {value}")

# for entry_num in sorted(mission_teams_dict.keys()):
#     print(f"{entry_num} ---")
#     for key, value in mission_teams_dict[entry_num].items():
#         print(f"\t{key} : {value}")
# долбайоб насрав закоментованого в мейн бренчу сука блять "ой а нахуя нам ото блять пуш в мастер сука"
# (мідл кстате 2.5 зпшка)
# він може коменти потім видалити но тіпа ця історія збережеться
print(json.dumps(mission_teams_dict, sort_keys=True, indent=4))

# якшо даня прочитав це то він ебать лох пізда