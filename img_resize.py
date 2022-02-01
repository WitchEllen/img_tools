import cv2
import os


def create_floder(file_dir):
    for class_path in os.listdir(file_dir):
        class_path = file_dir + '_re/' + class_path
        if not os.path.exists(class_path):
            os.mkdir(class_path)


def resize(file_dir):
    for class_path in os.listdir(file_dir):
        output_path = file_dir + '_re/' + class_path
        class_path = file_dir + '/' + class_path
        i = 0
        for img_name in os.listdir(class_path):
            image = cv2.imread(class_path + '/' + img_name)
            re = cv2.resize(image, (512, 512))
            cv2.imwrite(output_path + '/' + img_name.split('.')[0] + '.png',
                        re)
            i += 1
        print(i)


file_dir = 'src'
create_floder(file_dir)
resize(file_dir)
