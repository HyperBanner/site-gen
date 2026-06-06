import os
import shutil
from pathlib import Path


def main() -> None:
    copy_static_to_public()


def copy_static_to_public() -> None:
    source_dir = Path(__file__).resolve().parent.parent / "static"
    dest_dir = Path(__file__).resolve().parent.parent / "public"
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    print("Destination directory cleaned")
    copy_tree(source_dir, dest_dir)


# helper func for copy_static_to_public
def copy_tree(source_dir, dest_dir) -> None:
    items = os.listdir(source_dir)
    for item in items:
        item_path = os.path.join(source_dir, item)
        dest_item_path = os.path.join(dest_dir, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest_dir)
            print(f"Copied file to path: '{dest_item_path}' from: '{item_path}'")
        elif os.path.isdir(item_path):
            os.mkdir(dest_item_path)
            print(f"Made directory to path: '{dest_item_path}' from: '{item_path}'")
            copy_tree(item_path, dest_item_path)


if __name__ == "__main__":
    main()
