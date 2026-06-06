import unittest
from textnode import TextNode, TextType
from converter_functions import (
    text_node_to_html_node,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a codeblock node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a codeblock node")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode(
            "This is an image node", TextType.IMAGE, "/home/user/Pictures/picture.png"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "/home/user/Pictures/picture.png", "alt": "This is an image node"},
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_conversion(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )


class TestMarkdownToBlocks(unittest.TestCase):
    def test_conversion(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "# This is a heading"
        block2 = "## This is a heading"
        block3 = "### This is a heading"
        block4 = "#### This is a heading"
        block5 = "##### This is a heading"
        block6 = "###### This is a heading"
        block7 = "####### This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block2), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block3), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block4), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block5), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block6), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block7), BlockType.PARAGRAPH)

    def test_code(self):
        block = """```
This is a code block.
Imagine some code here.
```"""
        block2 = """```
This is an unclosed code block."""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        self.assertNotEqual(block_to_block_type(block2), BlockType.CODE)

    def test_quote(self):
        block = """> This is a quote block
> There will be quotes here.
>I don't need to put a space after the >."""
        block2 = """> This is a quote block.
Oops I forgot to put a > here.
> This time i remembered."""
        block3 = """> This is meant to be a quote block.
- I accidentally put a different thing at the start of the line.
> We are back to putting the correct symbol."""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        self.assertNotEqual(block_to_block_type(block2), BlockType.QUOTE)
        self.assertNotEqual(block_to_block_type(block3), BlockType.QUOTE)

    def test_ul(self):
        block = """- This is a list
- An unordered one
- This one doesn't involve numbers"""
        block2 = """- This is a list
Oh but oops i forgot the -
- Here i remembered"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type(block2), BlockType.UNORDERED_LIST)

    def test_ol(self):
        block = """1. This is an ordered list.
2. With incrementing numbers.
3. I know how to count."""
        block2 = """1. This is an ordered list.
3. This time, I don't know how to count
2. Don't blame me."""
        block3 = """1. This is an ordered list
2.I didn't put a space here.
3. I did put a space here."""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type(block2), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type(block3), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block = "This is just a normal paragraph."
        block2 = "# This is a heading tho."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        self.assertNotEqual(block_to_block_type(block2), BlockType.PARAGRAPH)


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
