import cv2
cap = cv2.VideoCapture(0)
cap.set(5, 25)
while (cap.isOpened()):
    frame_exists, curr_frame = cap.read()

    if frame_exists:
        print(cap.get(cv2.CAP_PROP_POS_MSEC))