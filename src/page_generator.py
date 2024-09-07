from block_markdown import markdown_to_html_node
import os
from pathlib import Path, PurePath

def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:]
    
    raise ValueError("No title found")



def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content = Path(dir_path_content)


    for entry in content.iterdir():
        if Path.is_file(entry):
            if str(entry).endswith(".md"):
                dest_path = os.path.join(dest_dir_path, "index.html")
                generate_page(entry, template_path, dest_path)
        else:
            current_dir = os.path.split(entry)[-1]
            new_dest_dir = os.path.join(dest_dir_path, current_dir)
            generate_pages_recursive(entry, template_path, new_dest_dir)
        



def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = get_file_contents(from_path)
    template = get_file_contents(template_path)
    
    page_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", page_html)
    
    dest_dir_path = os.path.split(dest_path)[0]

    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    with open(dest_path, "w") as f:
        f.write(template)
    

def get_file_contents(path):
    with open(path) as f:
        return f.read()