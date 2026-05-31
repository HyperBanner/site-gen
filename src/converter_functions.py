from enum import Enum
from htmlnode import LeafNode
from textnode import TextNode, TextType
from parsing import split_nodes_delimiter, split_nodes_image, split_nodes_link


# enum for block_to_block_type
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def text_node_to_html_node(text_node) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("TextNode must have a valid TextType")


def text_to_textnodes(text: str) -> list[TextNode]:
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    splitted = markdown.split("\n\n")
    for split in splitted:
        stripped = split.strip()
        if stripped != "":
            blocks.append(stripped)
    return blocks


def block_to_block_type(block: str) -> BlockType:
    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    count = 0
    for line in lines:
        if line.startswith(">"):
            count += 1
    if count == len(lines):
        return BlockType.QUOTE

    count = 0
    for line in lines:
        if line.startswith("- "):
            count += 1
    if count == len(lines):
        return BlockType.UNORDERED_LIST

    count = 0
    for i in range(1, len(lines) + 1):
        if lines[i - 1].startswith(f"{i}. "):
            count += 1
    if count == len(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
