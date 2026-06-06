import os
from converter_functions import markdown_to_html_node


def generate_pages_recursive(
    dir_path_content, template_path, dest_dir_path, basepath
) -> None:
    items = os.listdir(dir_path_content)
    for item in items:
        item_path = os.path.join(dir_path_content, item)
        dest_item_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(item_path):
            dest_item_path = dest_item_path.replace(".md", ".html")
            generate_page(item_path, template_path, dest_item_path, basepath)
        elif os.path.isdir(item_path):
            os.mkdir(dest_item_path)
            print(f"Made directory from path: '{item_path}' to: '{dest_item_path}'")
            generate_pages_recursive(item_path, template_path, dest_item_path, basepath)


# helper func for generate_pages_recursive
def generate_page(from_path, template_path, dest_path, basepath) -> None:
    print(f"Generating page from {from_path}, to {dest_path} using {template_path}")
    markdown = ""
    template = ""
    with open(from_path, "r") as file:
        markdown = file.read()
    with open(template_path, "r") as file:
        template = file.read()
    body = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = (
        template.replace("{{ Title }}", title)
        .replace("{{ Content }}", body)
        .replace('href="/', f'href="{basepath}/')
        .replace('src="/', f'src="{basepath}/')
    )

    # make sure dirs exist
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(page)


# helper func for generate_page
def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    header = ""
    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            header = line.lstrip("# ")
            break
    if not header:
        raise Exception("no title found")
    return header
