import string
import vdf


def get_steam_path():
    import sys
    import winreg

    hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Valve\Steam")
    path = winreg.QueryValueEx(hkey, "InstallPath")
    return path[0]


def findGame(gameIdToFind: string):
    vdfPath = get_steam_path() + "\steamapps\libraryfolders.vdf"
    vdfFile = vdf.load(open(vdfPath))
    steamLibs = vdfFile["libraryfolders"]
    for i in steamLibs:
        steamApps = steamLibs[i]["apps"]
        for gameId in steamApps:
            if gameId == gameIdToFind:
                return steamLibs[i]["path"]


if __name__ == "__main__":
    print(findGame("594650"))
