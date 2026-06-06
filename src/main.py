import os
import shutil
from pathlib import Path
from generator_functions import generate_page


def main() -> None:
    static = Path(__file__).resolve().parent.parent / "static"
    public = Path(__file__).resolve().parent.parent / "public"
    content = Path(__file__).resolve().parent.parent / "content" / "index.md"
    template = Path(__file__).resolve().parent.parent / "template.html"
    public_file = Path(__file__).resolve().parent.parent / "public" / "index.html"
    regenerate(static, public)
    generate_page(content, template, public_file)


def regenerate(static_dir, public_dir) -> None:
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
