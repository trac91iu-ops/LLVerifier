#!/bin/python3
import os
import re
import shutil
from collections import defaultdict

def cleanup_base(regexp,base_path, keep_latest_n):
    pattern = re.compile(regexp)
    grouped_paths = defaultdict(list)

    for entry in os.listdir(base_path):
        full_path = os.path.join(base_path, entry)
        #if os.path.isdir(full_path):
        match = pattern.match(entry)
        if match:
            prefix = match.group(1)
            timestamp = int(match.group(2))
            grouped_paths[prefix].append((timestamp, full_path))

    for prefix, paths in grouped_paths.items():
        # the newest to the oldest
        paths.sort(reverse=True)
        # keep latest N, delete others
        to_delete = paths[keep_latest_n:]
        for timestamp, path in to_delete:
            print(f"Deleting: {path}")
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)


def cleanup_grouped_folders(base_path, keep_latest_n):
    # match folders like "XXX.txt-<timestamp>"
    return cleanup_base(r'^(.+\.txt)-(\d+)$',base_path,keep_latest_n) 

def cleanup_logs(base_path, keep_latest_n):
    # match folders like "XXX.txt-<timestamp>"
    return cleanup_base(r'^(.+\.txt)-(\d+).txt$',base_path,keep_latest_n) 

if __name__ == "__main__":
    keep_latest_n = 2
    cleanup_grouped_folders('output', keep_latest_n)
    cleanup_logs('logs/', keep_latest_n)

