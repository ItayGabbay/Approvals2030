# -*- coding: utf-8 -*-
import serial
from time import sleep
import cv2
import os

GATE_SERIAL = serial.Serial(os.getenv('GATE_PORT', 'COM4'), 9600, timeout=0)


def take_picture(camera_index: int = 1):
    camera = cv2.VideoCapture(camera_index)
    return_value, image = camera.read()
    camera.release()
    if return_value:
        return image
    raise RuntimeError


def gate_open(ttl=4):
    sleep(2)
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
    GATE_SERIAL.write(bytes('r', encoding='ASCII'))
    sleep(ttl)
    GATE_SERIAL.write(bytes('o', encoding='ASCII'))

