import os
import shutil
import sys
from pathlib import Path
from generator_functions import generate_pages_recursive


def main() -> None:
    basepath = "/"
    if sys.argv:
        basepath = sys.argv[1]
    # paths
    static = Path(__file__).resolve().parent.parent / "static"
    docs = Path(__file__).resolve().parent.parent / "docs"
    content = Path(__file__).resolve().parent.parent / "content"
    template = Path(__file__).resolve().parent.parent / "template.html"

    setup_static_files(static, docs)
    generate_pages_recursive(content, template, docs, basepath)


def setup_static_files(static_dir, public_dir) -> None:
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.mkdir(public_dir)
    print("Destination directory cleaned")
    copy_tree(static_dir, public_dir)


# helper func for regenerate
def copy_tree(source_dir, dest_dir) -> None:
    items = os.listdir(source_dir)
    for item in items:
        item_path = os.path.join(source_dir, item)
        dest_item_path = os.path.join(dest_dir, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest_dir)
            print(f"Copied file from path: '{item_path}' to: '{dest_item_path}'")
        elif os.path.isdir(item_path):
            os.mkdir(dest_item_path)
            print(f"Made directory from path: '{item_path}' to: '{dest_item_path}'")
            copy_tree(item_path, dest_item_path)


if __name__ == "__main__":
    main()
