from datetime import datetime
import time

today = datetime.fromtimestamp(1660336160646607900 / 1000)

print(today.ctime())
