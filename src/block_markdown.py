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
    if block.startswith("# "):
        return "heading_1"
    
    if block.startswith("## "):
        return "heading_2"
    
    if block.startswith("### "):
        return "heading_3"
    
    if block.startswith("#### "):
        return "heading_4"
    
    if block.startswith("##### "):
        return "heading_5"
    
    if block.startswith("###### "):
        return "heading_6"
    
    if block.startswith("```") and block.endswith("```"):
        return "code"
    
    lines = block.split("\n")

    is_quote_block = all(line.startswith(">") for line in lines)
    if is_quote_block:
        return "quote"
    
    is_unordered_list = all(line.startswith("* ") or line.startswith("- ") for line in lines)
    if is_unordered_list:
        return "unordered_list"
    
    is_ordered_list = all(lines[i].startswith(f"{i + 1}. ") for i in range(len(lines)))
    if is_ordered_list:
        return "ordered_list"
    
    return "paragraph"