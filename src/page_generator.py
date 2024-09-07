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
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)
        


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