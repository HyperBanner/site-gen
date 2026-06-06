from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from parse_inline import split_nodes_delimiter, split_nodes_image, split_nodes_link


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


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        node = block_to_html_node(block)
        children.append(node)
    return ParentNode("div", children, None)


# helper funcs for markdown_to_html_node


def text_to_children(text: str) -> list[HTMLNode]:
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)

    match block_type:
        case BlockType.PARAGRAPH:
            lines = block.split("\n")
            paragraph = " ".join(lines)
            children = text_to_children(paragraph)
            return ParentNode("p", children)
        case BlockType.HEADING:
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break
            if level + 1 >= len(block):
                raise ValueError(f"invalid heading level: {level}")
            text = block[level + 1 :]
            children = text_to_children(text)
            return ParentNode(f"h{level}", children)
        case BlockType.CODE:
            if not block.startswith("```") or not block.endswith("```"):
                raise ValueError("invalid code block")
            text = block[4:-3]
            text_node = TextNode(text, TextType.TEXT)
            child = text_node_to_html_node(text_node)
            code = ParentNode("code", [child])
            return ParentNode("pre", [code])
        case BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                if not line.startswith(">"):
                    raise ValueError("invalid quote block")
                new_lines.append(line.lstrip(">").strip())
            content = " ".join(new_lines)
            children = text_to_children(content)
            return ParentNode("blockquote", children)
        case BlockType.ORDERED_LIST:
            items = block.split("\n")
            html_items = []
            for item in items:
                parts = item.split(". ", 1)
                text = parts[1]
                children = text_to_children(text)
                html_items.append(ParentNode("li", children))
            return ParentNode("ol", html_items)
        case BlockType.UNORDERED_LIST:
            items = block.split("\n")
            html_items = []
            for item in items:
                text = item[2:]
                children = text_to_children(text)
                html_items.append(ParentNode("li", children))
            return ParentNode("ul", html_items)
