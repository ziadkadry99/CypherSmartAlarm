import numpy as np
import cv2

cap = cv2.VideoCapture(0)


def get_frame():
    ret, frame = cap.read()
    return frame


def get_frame_grey():
    gray = cv2.cvtColor(get_frame(), cv2.COLOR_BGR2GRAY)
    return gray


def destruct():
    cap.release()
    cv2.destroyAllWindows()

