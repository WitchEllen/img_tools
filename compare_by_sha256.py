import hashlib
import os
import cv2
import numpy


def CalcFileSha256(filname):
    ''' calculate file sha256 '''
    with open(filname, 'rb') as f:
        sha256obj = hashlib.sha256()
        sha256obj.update(f.read())
        hash_value = sha256obj.hexdigest()
        return hash_value


def compare_by_sha256(src, dst):
    for filename in os.listdir(src):
        a = src + '/' + filename
        b = dst + '/' + filename
        if CalcFileSha256(a) != CalcFileSha256(b):
            print(filename)


def compare_by_rgb(src, dst):
    for filename in os.listdir(src):
        a = src + '/' + filename
        b = dst + '/' + filename
        diff = cv2.imread(a) - cv2.imread(b)
        # cv2.imwrite(filename, diff)
        d = numpy.sum(diff)
        print(filename + ' ' + str(d))


src = 'src'
dst = 'dst'
compare_by_sha256(src, dst)
