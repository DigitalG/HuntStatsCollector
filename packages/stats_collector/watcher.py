import time
import os
from typing import Callable


# Watcher that check files last modifier time with watch_delay in seconds
# If change is detected, wait until all changes is applied to avoid executing
# function for each quick change
# Calles function_to_execute with *args and **kwargs if changes is detected
def file_watcher(
    file_path_to_watch: str,
    watch_delay: int,
    function_to_execute: Callable,
    *args,
    **kwargs,
) -> None:
    modification_time = os.stat(file_path_to_watch).st_mtime
    expected_to_change = False
    print(f"Watcher | Starting watching | {file_path_to_watch}")

    while True:
        new_time = os.stat(file_path_to_watch).st_mtime
        if new_time != modification_time:
            expected_to_change = True
            modification_time = new_time
            print(f"Watcher | Changes found | {file_path_to_watch}")
        elif expected_to_change:
            print(f"Watcher | Function Executed | {file_path_to_watch}")
            function_to_execute(*args, **kwargs)
            expected_to_change = False
        time.sleep(watch_delay)
