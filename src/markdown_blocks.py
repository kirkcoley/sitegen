from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes
from htmlnode import HTMLNode, LeafNode, ParentNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == '':
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    if block.startswith("#"):
        for i in range(7):
            if block[i] == "#":
                continue
            if block[i] == " ":
                return BlockType.HEADING
            else:
                break
    if block.startswith("```"):
        if block.endswith("```"):
            return BlockType.CODE
    if block.startswith(">"):
        lines = block.splitlines()
        for i in range(len(lines)):
            if i == len(lines) - 1 and lines[i].startswith(">"):
                return BlockType.QUOTE
            if lines[i].startswith(">"):
                continue
            else:
                break
    if block.startswith("-"):
        lines = block.splitlines()
        for i in range(len(lines)):
            if i == len(lines) - 1 and lines[i].startswith("- "):
                return BlockType.UNORDERED_LIST
            if lines[i].startswith("- "):
                continue
            else:
                break
    if block.startswith("1"):
        lines = block.splitlines()
        for i in range(len(lines)):
            if i == len(lines) - 1 and lines[i].startswith(f"{i + 1}. "):
                return BlockType.ORDERED_LIST
            if lines[i].startswith(f"{i + 1}. "):
                continue
            else:
                break
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    raw_blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in raw_blocks:
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                nodes.append(ParentNode("p", text_to_children(block)))
            case BlockType.HEADING:
                nodes.append(ParentNode(f"h{block[:7].count('#')}", text_to_children(block)))
            case BlockType.CODE:
                text = TextNode(block.strip("```"), TextType.CODE)
                child = [text_node_to_html_node(text)]
                prenode = ParentNode("pre", child)
                nodes.append(prenode)
            case BlockType.QUOTE:
                lines = block.split("\n")
                clean_lines = []
                for line in lines:
                    clean_lines.append(line.lstrip(">").strip())
                new_block = " ".join(clean_lines)
                nodes.append(ParentNode("blockquote", text_to_children(new_block)))
            case BlockType.UNORDERED_LIST:
                items = md_list_to_html_list(block)
                nodes.append(ParentNode("ul", items))
            case BlockType.ORDERED_LIST:
                items = md_list_to_html_list(block)
                nodes.append(ParentNode("ol", items))
            case _:
                raise ValueError("invalid block type")
    return ParentNode("div", nodes)

def md_list_to_html_list(block):
    items = block.splitlines()
    html_list = []
    for item in items:
        html_list.append(LeafNode("li", item[2:].strip()))
    return html_list

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    htmlnodes = []
    for node in textnodes:
        htmlnodes.append(text_node_to_html_node(node))
    return htmlnodes
