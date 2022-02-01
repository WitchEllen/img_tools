import os.path
import cv2

for img_name in os.listdir('src'):
    image = cv2.imread('src/' + img_name)
    (h, w) = image.shape[:2]
    m = max(h, w)
    re = cv2.copyMakeBorder(image, (m - h) // 2 + 2,
                            m - (m - h) // 2 - h + 2, (m - w) // 2 + 2,
                            m - (m - w) // 2 - w + 2,
                            cv2.BORDER_CONSTANT,
                            value=[0, 0, 0])
    cv2.imwrite('dst/' + img_name.split('.')[0] + '.bmp', re)
