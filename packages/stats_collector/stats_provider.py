import json
import os
import copy
from datetime import datetime


class MatchStats:
    def __init__(self, data):
        self.accolade = data["accolade"]
        self.entries = data["entries"]
        self.teams = data["teams"]
        self.time = data["time"]

        self.monster_data_display_name_dict = {
            "kill grunt": "Grunts",
            "kill leeches": "Leeches",
            "kill hive": "Hives",
            "kill armored": "Armored",
            "kill hellhound": "Hellhounds",
            "kill waterdevil": "Waterdevils",
            "kill meathead": "Meatheads",
            "kill immolator": "Immolators",
        }

        self.hunters_data_display_name_dict = {
            "kill player mm rating 1 stars": "1 star",
            "kill player mm rating 2 stars": "2 stars",
            "kill player mm rating 3 stars": "3 stars",
            "kill player mm rating 4 stars": "4 stars",
            "kill player mm rating 5 stars": "5 stars",
            "kill player mm rating 6 stars": "6 stars",
        }

    def get_self_team_id(self):
        for id, team in self.teams.items():
            if team["ownteam"] == "true":
                return id

    def get_self_team(self):
        return self.teams[self.get_self_team_id()]

    def get_other_teams(self):
        other_teams = copy.deepcopy(self.teams)
        other_teams.pop(self.get_self_team_id())
        return other_teams

    def get_accolades_by_name(self, accolade_name: str, default_return={}):
        accolades = {
            k: v for k, v in self.accolade.items() if v["category"] == accolade_name
        }
        return accolades if accolades else default_return

    def get_entries_by_name(self, entry_name: str):
        return {k: v for k, v in self.entries.items() if v["category"] == entry_name}

    def get_monsters_stats(self):
        monsters_killed_accolade = self.get_accolades_by_name(
            "accolade_monsters_killed"
        )
        monsters_killed_entries = self.get_entries_by_name("accolade_monsters_killed")
        monsters_stats = {
            "monsters_killed": 0,
            "xp": 0,
            "blood_bonds": 0,
            "details": {},
        }
        for _, accolade in monsters_killed_accolade.items():
            monsters_stats["monsters_killed"] += int(accolade["hits"])
            monsters_stats["xp"] += int(accolade["xp"])
            monsters_stats["blood_bonds"] += int(accolade["generatedGems"])

        for _, entry in monsters_killed_entries.items():
            monster_name = self.monster_data_display_name_dict[entry["descriptorName"]]
            monsters_stats["details"][monster_name] = {
                "amount": entry["amount"],
                "xp": entry["rewardSize"],
            }
        return monsters_stats

    def get_hunters_data(self):
        hunters_killed_accolade = self.get_accolades_by_name("accolade_players_killed")
        hunters_killed_entries = self.get_entries_by_name("accolade_players_killed")
        hunters_stats = {
            "hunters_killed": 0,
            "xp": 0,
            "blood_bonds": 0,
            "details": {},
        }
        for _, accolade in hunters_killed_accolade.items():
            hunters_stats["hunters_killed"] += int(accolade["hits"])
            hunters_stats["xp"] += int(accolade["xp"])
            hunters_stats["blood_bonds"] += int(accolade["generatedGems"])

        for _, entry in hunters_killed_entries.items():
            monster_name = self.hunters_data_display_name_dict[entry["descriptorName"]]
            hunters_stats["details"][monster_name] = {
                "amount": entry["amount"],
                "xp": entry["rewardSize"],
            }
        return hunters_stats

    def get_blood_bonds(self):
        blood_bonds = 0
        for _, accolade in self.accolade.items():
            blood_bonds += int(accolade["generatedGems"])
        return blood_bonds

    def get_index_data(self):
        index_data = {}
        index_data.update({"date": self.time.ctime()})
        hunters_killed = self.get_hunters_data()["hunters_killed"]
        index_data.update({"hunters_killed": hunters_killed})
        monsters_killed = self.get_monsters_stats()["monsters_killed"]
        index_data.update({"monsters_killed": monsters_killed})
        blood_bonds = self.get_blood_bonds()
        index_data.update({"blood_bonds": blood_bonds})
        print(index_data)
        return index_data


class StatsProvider:
    data_path: str

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.matches = {}

        self.update()

    def update(self):
        matches_data_file_names = os.listdir(self.data_path)
        for file_name in matches_data_file_names:
            with open(f"{self.data_path}{file_name}", "r") as f:
                file_name_without_extension = file_name.split(".")[0]
                if file_name_without_extension not in self.matches.keys():
                    match_data = json.loads(f.read())
                    match_data["time"] = datetime.fromtimestamp(
                        int(file_name_without_extension)
                    )
                    self.matches.update(
                        {f"{file_name_without_extension}": MatchStats(match_data)}
                    )

    def get_match_by_id(self, id: int):
        return self.matches[id]

    def get_match_ids(self, page=1, per_page=0):

        if not isinstance(page, int):
            raise TypeError("page should be integer")
        if not isinstance(page, int):
            raise TypeError("per_page should be integer")

        if per_page <= 0:
            return self.matches.keys()
        if per_page >= 1 and page >= 1:
            return

    def get_index_data(self):
        index_data = {}
        for id, match_data in self.matches.items():
            index_data.update({id: match_data.get_index_data()})

        return index_data


if __name__ == "__main__":
    MATCHES_DATA_PATH = "data\\matches\\"
    provider = StatsProvider(MATCHES_DATA_PATH)
    print(provider.get_match_by_id("1660233357115068900").accolade)
    print(provider.get_match_by_id("1660233357115068900").entries)
    print(provider.get_match_by_id("1660233357115068900").teams)
    print(provider.get_match_ids())
