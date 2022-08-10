def get_steam_path():
    import sys
    import winreg

    hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Valve\Steam")
    path = winreg.QueryValueEx(hkey, "InstallPath")
    return path[0]


if __name__ == "__main__":
    print(get_steam_path())
