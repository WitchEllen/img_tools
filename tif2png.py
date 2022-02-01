from PIL import Image
import os


def create_floder(src, dst):
    for class_path in os.listdir(src):
        class_path = dst + '/' + class_path
        if not os.path.exists(class_path):
            os.mkdir(class_path)


def to_png(file_dir):
    for class_path in os.listdir(file_dir):
        print(class_path)
        output_path = file_dir + '_png/' + class_path
        class_path = file_dir + '/' + class_path
        i = 0
        for img_name in os.listdir(class_path):
            if img_name.split('.')[1].lower() == 'tif':
                im = Image.open(class_path + '/' + img_name)
                im.save(output_path + '/' + img_name.split('.')[0] + '.png')
                i += 1
        print(i)


src = 'origin'
dst = 'processed'
create_floder(src, dst)
to_png(src)
