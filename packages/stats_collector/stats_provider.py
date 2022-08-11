import json
import os


class MatchStats:
    def __init__(self, data):
        self.accolade = data["accolade"]
        self.entries = data["entries"]
        self.teams = data["teams"]


class StatsProvider:
    data_path: str

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.matches = {}

        matches_data_file_names = os.listdir(self.data_path)
        for file_name in matches_data_file_names:
            with open(f"{self.data_path}{file_name}", "r") as f:
                file_name_without_extension = file_name.split(".")[0]
                match_data = json.loads(f.read())
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


if __name__ == "__main__":
    MATCHES_DATA_PATH = "data\\matches\\"
    provider = StatsProvider(MATCHES_DATA_PATH)
    print(provider.get_match_by_id("1660233357115068900").accolade)
    print(provider.get_match_by_id("1660233357115068900").entries)
    print(provider.get_match_by_id("1660233357115068900").teams)
    print(provider.get_match_ids())
