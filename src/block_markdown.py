import re
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import ParentNode, LeafNode

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        nodes = block_to_html_node(block)
        children.append(nodes)

    return ParentNode("div", children)



def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []

    for block in blocks:
        if block == "":
            continue

        block = block.strip()
        filtered_blocks.append(block)

    return filtered_blocks



def block_to_block_type(block):
    lines = block.split("\n")
    
    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return block_type_heading

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code

    is_quote_block = all(line.startswith(">") for line in lines)
    if is_quote_block:
        return block_type_quote
    
    is_unordered_list = all(line.startswith("* ") or line.startswith("- ") for line in lines)
    if is_unordered_list:
        return block_type_ulist
    
    is_ordered_list = all(lines[i].startswith(f"{i + 1}. ") for i in range(len(lines)))
    if is_ordered_list:
        return block_type_olist
    
    return block_type_paragraph



def block_to_html_node(block):
    block_type = block_to_block_type(block)
    
    if block_type == block_type_paragraph:
        return paragraph_to_html_nodes(block)
    
    if block_type == block_type_heading:
        return heading_to_html_nodes(block)
    
    if block_type == block_type_code:
        return code_to_html_nodes(block)
    
    if block_type == block_type_quote:
        return quote_to_html_nodes(block)
    
    if block_type == block_type_olist:
        return olist_to_html_nodes(block)
    
    if block_type == block_type_ulist:
        return ulist_to_html_nodes(block)

    raise ValueError("Invalid block type")



def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []

    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)

    return children



def paragraph_to_html_nodes(paragraph_block):
    lines = paragraph_block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)



def heading_to_html_nodes(heading_block):
    heading_tag = get_heading_tag(heading_block)
    clean_text = heading_block.lstrip("# ")
    children = text_to_children(clean_text)
    return ParentNode(heading_tag, children)



def code_to_html_nodes(code_block):
    clean_text = code_block.strip("`\n")
    children = text_to_children(clean_text)
    code_node = ParentNode("code", children)
    return ParentNode("pre", [code_node])



def quote_to_html_nodes(quote_block):
    lines = quote_block.split("\n")
    clean_lines = []
    
    for line in lines:
        if line == "":
            continue
        clean_lines.append(line.strip(">").strip())

    quote = " ".join(clean_lines)
    children = text_to_children(quote)
    return ParentNode("blockquote", children)

        

def ulist_to_html_nodes(unordered_list_block):
    lines = unordered_list_block.split("\n")
    list_items = []
    
    for line in lines:
        if line == "":
            continue
        
        clean_line = line.lstrip("*- ")
        children = text_to_children(clean_line)
        list_items.append(ParentNode("li", children))

    return ParentNode("ul", list_items)



def olist_to_html_nodes(ordered_list_block):
    lines = ordered_list_block.split("\n")
    list_items = []
    
    for line in lines:
        if line == "":
            continue
        
        clean_line = line.lstrip("1234567890. ")
        children = text_to_children(clean_line)
        list_items.append(ParentNode("li", children))
        
    return ParentNode("ol", list_items)




def get_heading_tag(heading_block):
    hashtags = re.findall(r"^(#+) ", heading_block)
    
    if len(hashtags) == 0:
        raise ValueError("Input is not a heading block")

    heading_num = len(hashtags[0])
    heading_tag = f"h{heading_num}"
    return heading_tag





