import cv2
import numpy as np

croppingFlag = False
ix = -1
iy = -1

def cropper(event, x, y, flags, params):
    global croppingFlag, ix, iy
    if event == 1:
        croppingFlag = 1
        ix = x
        iy = y

    elif event == 4:
        croppingFlag = False
        cv2.rectangle(img, pt1=(ix, iy), pt2=(x, y), color=(0, 0, 255), thickness=2)
        croppedImg = img[iy:y, ix:x]
        cv2.imshow("window", croppedImg)

# Initialize an empty image
img = np.zeros((100, 100, 3), dtype=np.uint8)

cv2.namedWindow(winname="window")
cv2.setMouseCallback("window", cropper)

while True:
    cv2.imshow("window", img)
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

cv2.destroyAllWindows()
