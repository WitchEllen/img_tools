import cv2
import os.path
import numpy as np

L = 10
H = 4


def resize(image):
    (h, w) = image.shape[:2]
    m = max(h, w)
    re = cv2.copyMakeBorder(image, (m - h) // 2,
                            m - (m - h) // 2 - h, (m - w) // 2,
                            m - (m - w) // 2 - w,
                            cv2.BORDER_CONSTANT,
                            value=[0, 0, 0])
    return cv2.resize(re, (256, 256))


def merge(path):

    imageL = np.array([])
    imageF = np.array([])
    w = 0
    h = 0

    for fn in os.listdir(path):
        fp = path + '/' + fn

        image = resize(cv2.imread(fp))
        print(fp)

        if w < L - 1:
            if w == 0:
                imageL = image
            else:
                imageL = np.concatenate([imageL, image], axis=1)  # row
            w += 1
        else:
            imageL = np.concatenate([imageL, image], axis=1)  # row
            if h == 0:
                imageF = imageL
            else:
                imageF = np.concatenate([imageF, imageL], axis=0)  # column
            w = 0
            h += 1

    cv2.imwrite(path + '.png', imageF)
    return


path = 'src'
merge(path)
