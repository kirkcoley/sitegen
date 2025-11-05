import re
from textnode import TextNode, TextType, text_node_to_html_node


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if delimiter in node.text:
                split_list = node.text.split(delimiter)
                for i in range(len(split_list)):
                    if i % 2 != 0:
                        new_nodes.append(TextNode(split_list[i], text_type))
                    elif split_list[i] == '':
                        continue
                    else:
                        new_nodes.append(TextNode(split_list[i], TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
    

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
        else:
            sections = []
            image_helper(sections, images, node.text)
            for section in sections:
                if isinstance(section, tuple):
                    new_nodes.append(TextNode(section[0], TextType.IMAGE, section[1]))
                else:
                    new_nodes.append(TextNode(section, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
        else:
            sections = []
            link_helper(sections, links, node.text)
            for section in sections:
                if isinstance(section, tuple):
                    new_nodes.append(TextNode(section[0], TextType.LINK, section[1]))
                else:
                    new_nodes.append(TextNode(section, TextType.TEXT))
    return new_nodes

def image_helper(queue, images, text):
    sec = text.split(f"![{images[0][0]}]({images[0][1]})", 1)
    queue.append(sec.pop(0))
    queue.append(images.pop(0))
    if not images and sec[0] != '':
        queue.append(sec[-1])
        return
    if not sec or not images:
        return
    image_helper(queue, images, sec[0])

def link_helper(queue, links, text):
    sec = text.split(f"[{links[0][0]}]({links[0][1]})", 1)
    queue.append(sec.pop(0))
    queue.append(links.pop(0))
    if not links and sec[0] != '':
        queue.append(sec[-1])
        return
    if not sec or not links:
        return
    link_helper(queue, links, sec[0])

def text_to_textnodes(text):
    node1 = TextNode(text, TextType.TEXT)
    nodes = [node1]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
