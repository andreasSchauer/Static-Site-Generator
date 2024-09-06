from textnode import *
import os
import shutil
from copystatic import copy_contents


dir_path_static = "./static"
dir_path_public = "./public"


def main():
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    copy_contents("static", "public")


main()


"""



"""