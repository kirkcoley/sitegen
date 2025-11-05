import unittest

from inline_markdown import (
        split_nodes_delimiter,
        extract_markdown_images,
        extract_markdown_links,
        split_nodes_image,
        split_nodes_link,
        text_to_textnodes,
        )
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
                new_nodes, 
                [
                    TextNode("This is text with a ", TextType.TEXT), 
                    TextNode("bold", TextType.BOLD), 
                    TextNode(" word", TextType.TEXT)
                ]
            )

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
                new_nodes, 
                [
                    TextNode("This is text with a ", TextType.TEXT), 
                    TextNode("italic", TextType.ITALIC), 
                    TextNode(" word", TextType.TEXT)
                ]
            )

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
                new_nodes, 
                [
                    TextNode("This is text with a ", TextType.TEXT), 
                    TextNode("code block", TextType.CODE), 
                    TextNode(" word", TextType.TEXT)
                ]
            )
    
    def test_split_nodes_delimiter_start(self):
        node = TextNode("**Bold** beginning, regular end", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
                new_nodes,
                [
                    TextNode("Bold", TextType.BOLD),
                    TextNode(" beginning, regular end", TextType.TEXT)
                ]
            )
    
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertEqual(
                images,
                [
                    ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                    ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
                ]
            )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com)"
        links = extract_markdown_links(text)
        self.assertEqual(
                links,
                [
                    ("to boot dev", "https://www.boot.dev"),
                    ("to youtube", "https://www.youtube.com")
                ]
            )

    def test_split_images(self):
        node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
                [
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and another ", TextType.TEXT),
                    TextNode(
                        "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                        ),
                    ],
                new_nodes,
                )

    def test_split_links(self):
        node = TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com)",
                TextType.TEXT,
                )
        node2 = TextNode(
                "This is more text with a link [to google](https://www.google.com) and [to wikipedia](https://en.wikipedia.org) as well",
                TextType.TEXT,
                )
        nodelist = split_nodes_link([node, node2])
        self.assertListEqual(
                [
                    TextNode("This is text with a link ", TextType.TEXT),
                    TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("to youtube", TextType.LINK, "https://www.youtube.com"),
                    TextNode("This is more text with a link ", TextType.TEXT),
                    TextNode("to google", TextType.LINK, "https://www.google.com"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("to wikipedia", TextType.LINK, "https://en.wikipedia.org"),
                    TextNode(" as well", TextType.TEXT),
                    ],
                nodelist
                )

    def test_text_to_textnodes(self):
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
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ],
                nodes
            )

