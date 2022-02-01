import os
import exifread


def getExif(imgpath, filename):
    old_full_file_name = os.path.join(imgpath, filename)
    FIELD = 'EXIF DateTimeOriginal'
    fd = open(old_full_file_name, 'rb')
    tags = exifread.process_file(fd)
    fd.close()

    if FIELD in tags:
        new_name = 'IMG_' + str(tags[FIELD]).replace(':', '').replace(
            ' ', '_') + os.path.splitext(filename)[1]
        # 20181207_031034.jpg

        # 可对图片进行重命名
        new_full_file_name = os.path.join(imgpath, new_name)
        print(old_full_file_name, " ---> ", new_full_file_name)
        os.rename(old_full_file_name, new_full_file_name)
    else:
        print('No {} found'.format(FIELD), ' in: ', old_full_file_name)


def main(imgpath):
    for filename in os.listdir(imgpath):
        full_file_name = os.path.join(imgpath, filename)
        if os.path.isfile(full_file_name):
            getExif(imgpath, filename)
        elif os.path.isdir(full_file_name):
            main(full_file_name)


imgpath = "./other"
main(imgpath)
