import unittest

from htmlnode import LeafNode
from markdown_blocks import BlockType, markdown_to_blocks, block_to_block_type, text_to_children, markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
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

    def test_markdown_to_blocks_newlines(self):
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

    def test_block_to_block_type_heading(self):
        md = "# Heading"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_block_to_block_type_heading(self):
        md = "## Heading"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_block_to_block_type_heading(self):
        md = "### Heading"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_block_to_block_type_heading(self):
        md = "#### Heading"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_block_to_block_type_heading(self):
        md = "##### Heading"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_block_to_block_type_heading(self):
        md = "###### Heading"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        md = "```code block```"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.CODE)
        
    def test_block_to_block_type_multiline_code(self):
        md = """```code
block```"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        md = ">quote"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.QUOTE)

    def test_block_to_block_type_multiline_quote(self):
        md = """>multi
>line
>quote"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.QUOTE)
        
    def test_block_to_block_type_unordered_list(self):
        md = """- unordered
- list"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.UNORDERED_LIST)
        
    def test_block_to_block_type_ordered_list(self):
        md = """1. ordered
2. list"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.ORDERED_LIST)
        
    def test_block_to_block_type_paragraph(self):
        md = "paragraph"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_text_to_children(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        htmlnodes = text_to_children(text)
        self.assertEqual(
                htmlnodes,
                [
                    LeafNode(None, "This is "),
                    LeafNode("b", "text"),
                    LeafNode(None, " with an "),
                    LeafNode("i", "italic"),  
                    LeafNode(None, " word and a "),
                    LeafNode("code", "code block"),
                    LeafNode(None, " and an "),
                    LeafNode("image", '', {"src": "https://i.imgur.com/fJRm4Vk.jpeg", "alt": "obi wan image"}),
                    LeafNode(None, " and a "),
                    LeafNode("a", "link", {"href": "https://boot.dev"}),
                ]
            )

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
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
            )

    def test_codeblock(self):
        md = """
```This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
            )

    def test_unordered_list(self):
        md = """- item 1
- item 2
- item 3"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
                html,
                "<div><ul><li>item 1</li><li>item 2</li><li>item 3</li></ul></div>"
                )

    def test_ordered_list(self):
        md = """1. item 1
2. item 2
3. item 3"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
                html,
                "<div><ol><li>item 1</li><li>item 2</li><li>item 3</li></ol></div>"
                )
        pass

    def test_quote(self):
        md = """>This is
>a multiline
>quote"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
                html,
                "<div><blockquote>This is a multiline quote</blockquote></div>"
            )

if __name__ == "__main__":
    unittest.main()


