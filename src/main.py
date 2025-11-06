import os
import shutil
import sys
from textnode import TextType, TextNode
from generate_page import generate_page, generate_pages_recursive

def copy_content_r(source, dest):
    if not os.path.exists(source):
        raise Exception(f"{source} does not exist")
    if dest == "docs":
        print("Using rmtree to delete docs directory")
        shutil.rmtree(dest)
        os.mkdir("docs")
    cont = os.listdir(source)
    print(f"Contents of {source}:\n{cont}")
    for file in cont:
        name = os.path.join(source, file)
        if os.path.isfile(name):
            print(f"copying file {file} to {dest}")
            shutil.copy(name, dest)
        else:
            ndest = os.path.join(dest, file)
            print(f"creating directory {ndest}")
            os.makedirs(ndest, exist_ok=True)
            nsource = os.path.join(source, file)
            print("copying directory contents")
            copy_content_r(nsource, ndest)



def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    copy_content_r("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()
