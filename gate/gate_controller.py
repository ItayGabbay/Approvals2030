# -*- coding: utf-8 -*-
import serial
from time import sleep
import cv2
import os
from playsound import playsound
from gate.text_recognition import search_plates

GATE_SERIAL = serial.Serial(os.getenv('GATE_PORT', 'COM4'), 9600, timeout=0)

def take_car_num(camera_index: int = 1) -> str:
    video_capture = cv2.VideoCapture(camera_index)
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        plate = search_plates(frame)
        print(plate)
        if plate is not None:
            video_capture.release()
            cv2.destroyAllWindows()
            return plate

def take_face(camera_index: int = 0): #blocking
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    video_capture = cv2.VideoCapture(camera_index)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        if len(faces) > 0:
            video_capture.release()
            cv2.destroyAllWindows()
            return frame

def gate_open(ttl=4):
    sleep(2)
    playsound('yes.mp3', block=False)
    GATE_SERIAL.write(bytes('g', encoding='ASCII'))
    GATE_SERIAL.write(bytes('0', encoding='ASCII'))  # open
    sleep(ttl)
    GATE_SERIAL.write(bytes('1', encoding='ASCII'))  # close
    GATE_SERIAL.write(bytes('o', encoding='ASCII'))


def unrecognized(ttl=2):
    sleep(2)
    GATE_SERIAL.write(bytes('b', encoding='ASCII'))
    sleep(ttl)
    GATE_SERIAL.write(bytes('o', encoding='ASCII'))


def unauthorized(ttl=2):
    sleep(2)
    playsound('nope.mp3', block=False)
    GATE_SERIAL.write(bytes('r', encoding='ASCII'))
    sleep(ttl)
    GATE_SERIAL.write(bytes('o', encoding='ASCII'))

if __name__ == '__main__':
    take_car_num()