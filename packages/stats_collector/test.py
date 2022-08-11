import difflib
import time

d = difflib.Differ()

diff = d.compare(["123123123---123123"], ["123123123123123123"])
with open("compare.txt", "w") as f:
    f.writelines(diff)
