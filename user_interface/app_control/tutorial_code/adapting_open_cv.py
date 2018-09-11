import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('audiveris_gui.png',0)
img2 = img.copy()
template = cv2.imread('file_button.png',0)
w, h = template.shape[::-1]

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

method = eval('cv2.TM_CCOEFF')
res = cv2.matchTemplate(img, template, method)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)
print(top_left)
print(bottom_right)

cv2.rectangle(img,top_left, bottom_right, (0,0,255), 2)

plt.subplot(121),plt.imshow(res, cmap = 'gray')
plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(img, cmap = 'gray')
plt.title('Detected Point'),plt.xticks([]), plt.yticks([])
plt.suptitle(method)

plt.show()
