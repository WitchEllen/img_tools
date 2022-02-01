import os

root_path = 'src/'
new_root_path = 'dst/'
for dir_name in os.listdir(root_path):
    if not os.path.exists(new_root_path + dir_name):
        os.mkdir(new_root_path + dir_name)
