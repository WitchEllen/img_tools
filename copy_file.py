from shutil import copyfile
import os

root_path = 'src/'
new_root_path = 'dst/'
for dir_name in os.listdir(root_path):
    class_path = dir_name.split('-')[0]
    if not os.path.exists(new_root_path + class_path):
        os.mkdir(new_root_path + class_path)
    for img_name in os.listdir(root_path + dir_name):
        copyfile(root_path + dir_name + '/' + img_name,
                 new_root_path + class_path + '/' + img_name)
