import os


def find_nearest_file(target_file="main.py"):
    """Find the nearest target file traversing recursively up the folder structure."""

    current_dir = os.path.dirname(os.path.abspath(__file__))
    while True:

        target_path = os.path.join(current_dir, target_file)
        print(f"Searching for {target_path} in {current_dir}")
        if os.path.exists(target_path):
            return current_dir
        else:
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                raise FileNotFoundError(f"Couldn't find {target_file}")

        current_dir = parent_dir
