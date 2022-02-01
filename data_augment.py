import cv2
import copy

import numpy as np
from scipy.ndimage.interpolation import map_coordinates
from scipy.ndimage.filters import gaussian_filter

PATCH = 2

# 步骤：拉伸-弹性-方形化-旋转-镜像


# 弹性变换
# alpha越小，sigma越大，产生的偏差越小，和原图越接近
def Elastic_transform(image, alpha, sigma, random_state=None):
    if random_state is None:
        random_state = np.random.RandomState(None)
    shape = image.shape
    shape_size = shape[:2]
    dx = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma) * alpha
    dy = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma) * alpha
    dz = np.zeros_like(dx)

    x, y, z = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]),
                          np.arange(shape[2]))
    indices = np.reshape(y + dy,
                         (-1, 1)), np.reshape(x + dx,
                                              (-1, 1)), np.reshape(z, (-1, 1))

    return map_coordinates(image, indices, order=1,
                           mode='reflect').reshape(shape)


# 随机仿射弹性变换
def elastic_transform(image, alpha, sigma, alpha_affine, random_state=None):
    if random_state is None:
        random_state = np.random.RandomState(None)

    shape = image.shape
    shape_size = shape[:2]

    # Random affine
    center_square = np.float32(shape_size) // 2
    square_size = min(shape_size) // 3
    pts1 = np.float32([
        center_square + square_size,
        [center_square[0] + square_size, center_square[1] - square_size],
        center_square - square_size
    ])
    pts2 = pts1 + random_state.uniform(
        -alpha_affine, alpha_affine, size=pts1.shape).astype(np.float32)
    M = cv2.getAffineTransform(pts1, pts2)
    image = cv2.warpAffine(image,
                           M,
                           shape_size[::-1],
                           borderMode=cv2.BORDER_REFLECT_101)

    dx = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma) * alpha
    dy = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma) * alpha
    dz = np.zeros_like(dx)

    x, y, z = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]),
                          np.arange(shape[2]))
    indices = np.reshape(y + dy,
                         (-1, 1)), np.reshape(x + dx,
                                              (-1, 1)), np.reshape(z, (-1, 1))

    return map_coordinates(image, indices, order=1,
                           mode='reflect').reshape(shape)


# 旋转
def rotate(image, angle, center=None, scale=1.0):
    (h, w) = image.shape[:2]
    # If no rotation center is specified, the center of the image is set as the rotation center
    if center is None:
        center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated


# 镜像
def mirror(image):
    size = image.shape
    # Get an image that is the same as the original image, note this to use deep copy
    iLR = copy.deepcopy(image)
    h = size[0]
    w = size[1]
    for i in range(h):  # row and col
        for j in range(w):
            iLR[i, w - 1 - j] = image[i, j]  # Mirror formula
    return iLR


# 拉伸
def resize(image, fx=1.0, fy=1.0):
    size = image.shape
    h = size[0]
    w = size[1]
    return cv2.resize(image, (int(w * fx), int(h * fy)))


# 正方形化
def squ_ize(image):
    border = 4
    (h, w) = image.shape[:2]
    m = max(h, w)
    re = cv2.copyMakeBorder(image, (m - h) // 2 + border,
                            m - (m - h) // 2 - h + border,
                            (m - w) // 2 + border,
                            m - (m - w) // 2 - w + border,
                            cv2.BORDER_CONSTANT,
                            value=[0, 0, 0])
    return re


def exe_increser(file_dir, output_path, file_list_name, process_record,
                 image_type):

    p = open(process_record, 'r')
    process_base = int(p.readline())
    p.close()

    f = open(file_list_name, 'r')
    image_list = f.readline().split(' ')
    f.close()

    rest = len(image_list) - process_base

    for processed in range(rest):
        img_name = image_list[processed + process_base]
        image = cv2.imread(file_dir + '/' + img_name + image_type)
        class_path = output_path + '/' + img_name.split('-')[0]
        # img_name = img_name.split('.')[0]

        # if not os.path.exists(class_path):
        #     os.mkdir(class_path)

        for fx in (1.0, 1.1, 1.2):  # x轴缩放因子
            for fy in (1.0, 1.1, 1.2):  # y轴缩放因子
                if (fx != 1.0 and fx == fy):
                    continue
                re = resize(image, fx, fy)  # 拉伸
                for alpha in (1, 2, 3, 4):
                    for sigma in (0.1, 0.15):
                        im_et = Elastic_transform(re, re.shape[1] * alpha,
                                                  re.shape[1] * sigma)
                        im_et_sq = squ_ize(im_et)  # 方形化
                        iLR = mirror(im_et_sq)  # 镜像
                        cv2.imwrite(
                            class_path + '/' + img_name + '_' + str(fx) + '_' +
                            str(fy) + '_' + str(alpha) + '_' + str(sigma) +
                            '.png', im_et_sq)
                        cv2.imwrite(
                            class_path + '/' + img_name + '_' + str(fx) + '_' +
                            str(fy) + '_' + str(alpha) + '_' + str(sigma) +
                            '_mirr.png', iLR)

        print(str(process_base + processed) + ' ' + img_name)
        p = open(process_record, 'w')
        p.write(str(process_base + processed + 1))
        p.close()
    return


file_list_name = 'FileList.txt'
process_record = 'ProcessRecord.txt'
file_dir = 'src'
output_path = 'dst'
image_type = '.png'
exe_increser(file_dir, output_path, file_list_name, process_record, image_type)
