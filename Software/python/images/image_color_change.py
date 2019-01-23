import cv2
import numpy as np
img = cv2.imread(r"flat.png", cv2.IMREAD_UNCHANGED)
height, width, depth = img.shape

#print(img[0][0])
#print(type(img[0][0]))


# Treble Clef Filter
for i in range(0,height):
    for j in range(0, width):
        if img[i,j][3] == 0:
            continue
        else:
            #green
            #img[i,j][1] = 70
            # yellow
            img[i,j][1] = 70
            img[i,j][2] = 70
            # violet
            #img[i,j][0] = 255
            #img[i,j][2] = 130
            # cyan
            #img[i,j][0] = 70
            #img[i,j][1] = 70
            pass


cv2.imshow("input", img)

k = cv2.waitKey(0)

if k == ord('s'):
    cv2.imwrite('yellow_flat_shaded.png', img)
cv2.destroyAllWindows()
