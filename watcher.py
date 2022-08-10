import time
import os
from typing import Callable


def file_watcher(
    file_path_to_watch: str,
    watch_delay: int,
    function_to_execute: Callable,
    *args,
    **kwargs,
) -> None:
    modification_time = os.stat(file_path_to_watch).st_mtime

    print(f"Starting watching | {file_path_to_watch}")

    while True:
        new_time = os.stat(file_path_to_watch).st_mtime
        if new_time != modification_time:
            modification_time = new_time
            print(f"Changes found | {file_path_to_watch}")
            function_to_execute(*args, **kwargs)
        time.sleep(watch_delay)
