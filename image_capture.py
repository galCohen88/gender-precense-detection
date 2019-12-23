import cv2


def take_picture(img_name):
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cv2.imwrite(img_name, frame)
    print("{} written!".format(img_name))
    cam.release()
    cv2.destroyAllWindows()
