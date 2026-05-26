import unittest
from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
