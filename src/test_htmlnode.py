import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is a paragraph", None, None)
        node2 = HTMLNode("p", "This is a paragraph", None, None)
        self.assertEqual(node, node2)

    def test_tag_different(self):
        node = HTMLNode("a", "This is a paragraph", None, None)
        node2 = HTMLNode("p", "This is a paragraph", None, None)
        self.assertNotEqual(node, node2)

    def test_value_different(self):
        node = HTMLNode("p", "This is a paragraph", None, None)
        node2 = HTMLNode("p", "This is another paragraph", None, None)
        self.assertNotEqual(node, node2)


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "This is a paragraph", None)
        node2 = LeafNode("p", "This is a paragraph", None)
        self.assertEqual(node, node2)

    def test_different(self):
        node = LeafNode("a", "This is a paragraph", None)
        node2 = LeafNode("p", "This is a paragraph", None)
        self.assertNotEqual(node, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "This is a link", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">This is a link</a>'
        )

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "This is the headline", {"class": "header", "id": "h1"})
        self.assertEqual(
            node.to_html(), '<h1 class="header" id="h1">This is the headline</h1>'
        )


if __name__ == "__main__":
    unittest.main()
