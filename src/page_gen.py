import os
import shutil

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path,"r") as from_file:
        markdown = from_file.read()
    with open(template_path, "r") as template:
        template_content = template.read()
    md_nodes = markdown_to_html_node(markdown)
    md_string = md_nodes.to_html()
    title = extract_title(markdown)
    template_content.replace(f"{{ Title }}", title)
    template_content.replace(f"{{ Content }}", md_string)
    with open(dest_path, "x") as page:
        page.write(template_content)
