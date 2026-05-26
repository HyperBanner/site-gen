import unittest
from parsing import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_one_passthrough(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_two_passthroughs(self):
        node = TextNode(
            "This is text with a `code block` and a **bold phrase** in it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and a ", TextType.TEXT),
                TextNode("bold phrase", TextType.BOLD),
                TextNode(" in it", TextType.TEXT),
            ],
        )

    def test_three_passthroughs(self):
        node = TextNode(
            "This is text with a `code block`, a **bold phrase**, and an _italic phrase_ in it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(", a ", TextType.TEXT),
                TextNode("bold phrase", TextType.BOLD),
                TextNode(", and an ", TextType.TEXT),
                TextNode("italic phrase", TextType.ITALIC),
                TextNode(" in it", TextType.TEXT),
            ],
        )


if __name__ == "__main__":
    unittest.main()
