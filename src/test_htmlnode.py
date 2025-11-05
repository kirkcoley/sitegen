import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank",})
        node_props = node.props_to_html()
        self.assertEqual(node_props, ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_eq(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank",})
        node2 = HTMLNode(props={"href": "https://www.google.com", "target": "_blank",})
        node_props = node.props_to_html()
        node2_props = node2.props_to_html()
        self.assertEqual(node_props, node2_props)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Google", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Google</a>')

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

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

    def test_to_html_with_children_with_props(self):
        child_node = LeafNode("a", "Google", {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><a href="https://www.google.com">Google</a></div>')
    
    def test_to_html_with_grandchildren_with_props(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("p", [grandchild_node], {"hidden": ""})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
                parent_node.to_html(),
                "<div><p hidden><b>grandchild</b></p></div>",
                )
