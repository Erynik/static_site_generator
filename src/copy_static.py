import os
import shutil


def copy_static_tree(source: str, dest: str):
    # step 1: Delete all contents of /public and regenerate the folder itself
    if not os.path.exists(source):
        RaiseException("Source path does not exist.")
    shutil.rmtree(f"{dest}/", ignore_errors=True)
    if not os.path.exists(dest):
        os.mkdir(dest)
    print(f"Destination path cleared.")
    # step 2: copy all files and subdirectories, nested files
    source_list = os.listdir(source)
    for item in source_list:
        item_path = os.path.join(source, item)
        print(f"Item path: {item_path}")
        dest_path = os.path.join(dest, item)
        print(f"Desination path: {dest_path}")
        if os.path.isfile(item_path):
            print(f"{item} is file, copying to destination.")
            shutil.copy(item_path, dest_path)
            print(f"{item} copied.")
        else:
            print(f"{item} is directory, copying folder and recursing.")
            copy_static_tree(item_path, dest_path)