import os
import shutil

from copy_static import copy_static_tree
from markdown_code import extract_title
from page_gen import generate_page

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    copy_static_tree(dir_path_static, dir_path_public)
    generate_page("content/index.md", "template.html", f"{dir_path_public}/index.html")



main()
