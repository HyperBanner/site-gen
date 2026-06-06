import os
from converter_functions import markdown_to_html_node


def generate_page(from_path, template_path, dest_path) -> None:
    print(f"Generating page from {from_path}, to {dest_path} using {template_path}")
    markdown = ""
    template = ""
    with open(from_path, "r") as file:
        markdown = file.read()
    with open(template_path, "r") as file:
        template = file.read()
    body = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", body)

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
