import re
from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType) -> list:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        splitted = old_node.text.split(delimiter)
        if len(splitted) % 2 == 0:
            raise Exception("Invalid markdown syntax: unclosed delimiter")
        for i in range(len(splitted)):
            if splitted[i] != "":
                if i % 2 == 0:
                    new_nodes.append(TextNode(splitted[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(splitted[i], text_type))
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if (
            not extract_markdown_images(old_node.text)
            or old_node.text_type != TextType.TEXT
        ):
            new_nodes.append(old_node)
            continue
        matches = extract_markdown_images(old_node.text)
        text = old_node.text
        for match in matches:
            sections = text.split(f"![{match[0]}]({match[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if (
            not extract_markdown_links(old_node.text)
            or old_node.text_type != TextType.TEXT
        ):
            new_nodes.append(old_node)
            continue
        matches = extract_markdown_links(old_node.text)
        text = old_node.text
        for match in matches:
            sections = text.split(f"[{match[0]}]({match[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


# helper functions for split_nodes_image and split_nodes_link respectively
def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
