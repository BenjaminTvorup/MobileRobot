import numpy as np
import cv2

width = 100
height = 100
img = 255 * np.ones((height, width), dtype=np.uint8)
cv2.imwrite('empty_map.pgm', img)