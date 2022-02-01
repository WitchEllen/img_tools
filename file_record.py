import os


def gen_filelist(path, filename):
    file = open(filename, 'w')
    class_name = os.listdir(path)
    class_name.sort()
    for cp in class_name:
        file_name = os.listdir(path + '/' + cp)
        file_name.sort()
        for fn in file_name:
            file.write(cp + '/' + fn + ' ')
    file.close()


def read_filelist(filename):
    file = open(filename, 'r')

    mstr = file.readline()
    file_list = mstr.split(' ')
    print(len(file_list))

    file.close()
    return file_list


def gen_resultlist(path, filename):
    file = open(filename, 'w')
    class_name = os.listdir(path)
    class_name.sort()
    for cp in class_name:
        file_name = os.listdir(path + '/' + cp)
        file_name.sort()
        for fn in file_name:
            file.write(fn + ' ')
    file.close()


filename = 'ResultList.txt'
path = 'src'
gen_resultlist(path, filename)
