import os
from markdown_blocks import extract_title, markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = ''
    template = ''
    with open(from_path) as file:
        md = file.read()
    with open(template_path) as file:
        template = file.read()
    title = extract_title(md)
    html = markdown_to_html_node(md).to_html()
    doc = template.replace("{{ Title }}", title)
    doc = doc.replace("{{ Content }}", html)
    with open(dest_path, "w") as file:
        file.write(doc)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    cont = os.listdir(dir_path_content)
    for file in cont:
        sname = os.path.join(dir_path_content, file)
        dname = os.path.join(dest_dir_path, file)
        if os.path.isfile(sname):
            if sname.endswith(".md"):
                generate_page(sname, template_path, dname.replace("md", "html"))
            else:
                continue
        else:
            if not os.path.exists(dname):
                os.mkdir(dname)
            generate_pages_recursive(sname, template_path, dname)
