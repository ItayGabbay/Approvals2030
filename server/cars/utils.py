# -*- coding: utf-8 -*-
import cv2

CONST_MARGINS = 70

def extract_face(frame: bytearray):
    img = cv2.imdecode(frame, 0)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    if len(faces) > 0:
        f = faces[0]
        x, y, w, h = [v for v in f]
        sub_face = img[y-CONST_MARGINS:y + h + CONST_MARGINS, x-CONST_MARGINS:x + w + CONST_MARGINS]
        return sub_face
    return None
