import os
import shutil

from copy_static import copy_static_tree
from markdown_code import extract_title

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    copy_static_tree(dir_path_static, dir_path_public)

    


main()
