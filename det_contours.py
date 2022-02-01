import cv2
import os
import numpy as np


def get_contours(file_dir, output_dir):
    for img_name in os.listdir(file_dir):
        img = cv2.imread(file_dir + '/' + img_name)
        img_name = img_name.split('.')[0]
        h, w = img.shape[:2]

        # 进行滤波去掉噪声
        blured = cv2.blur(img, (5, 5))
        # 掩码长和宽都比输入图像多两个像素点，泛洪填充不会超出掩码的非零边缘
        mask = np.zeros((h + 2, w + 2), np.uint8)
        # 进行泛洪填充
        cv2.floodFill(blured, mask, (w - 1, h - 1), (255, 255, 255), (2, 2, 2),
                      (3, 3, 3), 8)
        # 得到灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 定义结构元素
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 50))
        # 开闭运算，先开运算去除背景噪声，再继续闭运算填充目标内的孔洞
        # opened = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
        # closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

        # 求二值图
        ret, binary = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)

        # 找到轮廓
        # cv2.RETR_EXTERNAL表示只检测外轮廓
        # cv2.RETR_LIST检测的轮廓不建立等级关系
        # cv2.RETR_CCOMP建立两个等级的轮廓，上面的一层为外边界，里面的一层为内孔的边界信息。如果内孔内还有一个连通物体，这个物体的边界也在顶层。
        # cv2.RETR_TREE建立一个等级树结构的轮廓。
        _, contours, hierarchy = cv2.findContours(binary, cv2.RETR_LIST,
                                                  cv2.CHAIN_APPROX_NONE)

        wimg = np.zeros([h, w, 3], np.uint8) + 255
        cv2.drawContours(wimg, contours, -1, (0, 0, 0), 1)

        # 绘制结果
        cv2.imwrite(output_dir + '/' + img_name + '_con.png', wimg)


file_dir = 'Image_Increase/original_test'
output_dir = 'Image_Increase/original_test'
get_contours(file_dir, output_dir)
