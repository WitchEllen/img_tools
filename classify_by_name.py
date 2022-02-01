import os.path
import shutil


def classify(file_dir, output_path):

    for img_name in os.listdir(file_dir):
        srcfile = file_dir + '/' + img_name
        class_path = output_path + '/' + img_name.split('-')[0]
        dstfile = class_path + '/' + img_name

        if not os.path.exists(class_path):
            os.mkdir(class_path)

        shutil.copyfile(srcfile, dstfile)
    return


file_dir = 'src'
output_path = 'dst'
classify(file_dir, output_path)
