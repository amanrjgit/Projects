import cv2
import pandas as pd


face = cv2.CascadeClassifier('casscade/haarcascade_frontalface_alt2.xml')

cap = cv2.VideoCapture(0)

while True:
    _,frame = cap.read()
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(grey, scaleFactor=1.5, minNeighbors=5)
    for (x, y, w, h) in faces:
        # print(x,y,w,h)
        roi_gray = grey[y:y + h, x:x + w]  # (ycord_start, ycord_end)
        roi_color = frame[y:y + h, x:x + w]

        color = (255, 0, 0)  # BGR 0-255
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

    cv2.imshow('Virtual Mouse', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break