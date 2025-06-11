# file_search.py
# Placeholder for file search utility functions 

import os

def search_files(query, search_dirs=None, max_results=10):
    if search_dirs is None:
        user_folder = os.path.expanduser("~")
        search_dirs = [
            os.path.join(user_folder, "Documents"),
            os.path.join(user_folder, "Desktop"),
            os.path.join(user_folder, "Downloads"),
        ]
    matches = []
    query_lower = query.lower()
    for base_dir in search_dirs:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if query_lower in file.lower():
                    matches.append(os.path.join(root, file))
                    if len(matches) >= max_results:
                        return matches
    return matches 