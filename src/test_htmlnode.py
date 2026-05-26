import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren_props(self):
        grandchild_node = LeafNode("b", "grandchild", {"class": "bold"})
        child_node = ParentNode("span", [grandchild_node], {"class": "highlight"})
        parent_node = ParentNode("div", [child_node], {"class": "box"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="box"><span class="highlight"><b class="bold">grandchild</b></span></div>',
        )


if __name__ == "__main__":
    unittest.main()
