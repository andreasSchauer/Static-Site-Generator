import os
import shutil

def copy_contents(src_dir_path, dst_dir_path):
    if not os.path.exists(dst_dir_path):
        os.mkdir(dst_dir_path)

    src_contents = os.listdir(src_dir_path)

    for filename in src_contents:
        from_path = os.path.join(src_dir_path, filename)
        dest_path = os.path.join(dst_dir_path, filename)

        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_contents(from_path, dest_path)