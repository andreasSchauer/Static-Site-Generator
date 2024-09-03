from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
)
import re


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    delimiters = ["**", "*", "`"]

    if delimiter not in delimiters:
        raise ValueError("Invalid Markdown Syntax: Delimiter not supported")
    
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        
        split_text = node.text.split(delimiter)
        nodes_to_add = []
            
        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            elif i % 2 == 0:
                nodes_to_add.append(TextNode(split_text[i], text_type_text))
            else:
                nodes_to_add.append(TextNode(split_text[i], text_type))

        new_nodes.extend(nodes_to_add)

    return new_nodes


def extract_markdown_images(text):
    image_regex = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(image_regex, text)
    return matches

def extract_markdown_links(text):
    link_regex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(link_regex, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        
        images = extract_markdown_images(node.text)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        split_text = re.split(r"!\[.*?\]\(.*?\)", node.text)
        nodes_to_add = []

        for i in range(len(split_text)):
            if split_text[i] != "":
                nodes_to_add.append(TextNode(split_text[i], text_type_text))
            
            if i < len(images):
                image_alt = images[i][0]
                image_link = images[i][1]
                nodes_to_add.append(TextNode(image_alt, text_type_image, image_link))

        new_nodes.extend(nodes_to_add)

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        
        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        split_text = re.split(r"(?<!!)\[.*?\]\(.*?\)", node.text)
        nodes_to_add = []

        for i in range(len(split_text)):
            if split_text[i] != "":
                nodes_to_add.append(TextNode(split_text[i], text_type_text))
            
            if i < len(links):
                link_text = links[i][0]
                link_url = links[i][1]
                nodes_to_add.append(TextNode(link_text, text_type_link, link_url))

        new_nodes.extend(nodes_to_add)

    return new_nodes
