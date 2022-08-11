import string
import vdf

# gets path to Steam folder
def get_main_steam_path() -> str:
    import sys
    import winreg

    hkey = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WOW6432Node\\Valve\\Steam"
    )
    path = winreg.QueryValueEx(hkey, "InstallPath")
    return path[0]


# get path to location where game with game_id_to_find is located
def get_steam_library_path_for_game_id(game_id_to_find: string) -> str:
    vdf_path = get_main_steam_path() + "\\steamapps\\libraryfolders.vdf"
    vdf_file = vdf.load(open(vdf_path))
    steam_libs = vdf_file["libraryfolders"]
    for _, value in steam_libs.items():
        steam_apps = value["apps"]
        for game_id in steam_apps:
            if game_id == game_id_to_find:
                return value["path"]


if __name__ == "__main__":
    print(get_steam_library_path_for_game_id("594650"))
