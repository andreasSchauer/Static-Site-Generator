from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
)


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