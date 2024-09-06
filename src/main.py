from textnode import *
import os
import shutil

def main():
    textnode = TextNode("dummy thicc node", text_type_bold, "https://boot.dev")
    copy_contents("static", "public")



def copy_contents(src_path, dst_path):
    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)
        os.mkdir(dst_path)
    else:
        os.mkdir(dst_path)

    src_contents = os.listdir(src_path)

    for path in src_contents:
        current_path = os.path.join(src_path, path)

        if os.path.isfile(current_path):
            shutil.copy(current_path, dst_path)
        else:
            new_destination = os.path.join(dst_path, path)
            copy_contents(current_path, new_destination)



copy_contents("static", "public")

main()


"""

os.path.exists(path) => returns True if path exists

os.listdir(path) => returns list containing the names of the entries in the directory given by path

os.path.join(path, *path) => joins one or more path components intelligently (with / added between them)

os.path.isfile(path) => returns True if path is an existing regular file

os.mkdir(path) => create a directory named path

shutil.copy(source, destination) => copies the file called source to the file or directory called destination 

shutil.rmtree(path) => delete an entire directory tree

"""