import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_default_url(self):
        node = TextNode("Test", TextType.TEXT, "https://google.com")
        node2 = TextNode("Test", TextType.TEXT)
        self.assertNotEqual(node.url, node2.url)

    def test_text_type(self):
        node = TextNode("Test", TextType.ITALIC)
        node2 = TextNode("Test", TextType.TEXT)
        self.assertNotEqual(node.text_type, node2.text_type)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node(self):
        text_node = TextNode("Test", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        comp_html_node = LeafNode("code", "Test")
        self.assertEqual(html_node, comp_html_node)



if __name__ == "__main__":
    unittest.main()
