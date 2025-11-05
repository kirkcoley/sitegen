import os
import shutil
from textnode import TextType, TextNode
from generate_page import generate_page, generate_pages_recursive

def copy_content_r(source, dest):
    if not os.path.exists(source):
        raise Exception(f"{source} does not exist")
    if dest == "public":
        print("Using rmtree to delete public directory")
        shutil.rmtree(dest)
        os.mkdir("public")
    cont = os.listdir(source)
    print(f"Contents of {source}:\n{cont}")
    for file in cont:
        name = os.path.join(source, file)
        if os.path.isfile(name):
            print(f"copying file {file} to {name}")
            shutil.copy(name, dest)
        else:
            ndest = os.path.join(dest, file)
            print(f"creating directory {ndest}")
            os.mkdir(ndest)
            nsource = os.path.join(source, file)
            print("copying directory contents")
            copy_content_r(nsource, ndest)



def main():
    copy_content_r("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()
