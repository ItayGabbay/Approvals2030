# -*- coding: utf-8 -*-
from json import loads
from gate.gate_controller import *
import os
import requests
import cv2
import jsonpickle

MAIN_SERVER_HOST = os.getenv('GATE_SERVICE_ADDR', 'http://127.0.0.1:8080')
MAIN_SERVER_REQUEST = f'{MAIN_SERVER_HOST}/api/validatePerson'

FACE_CAMERA_INDEX = 0
CAR_CAMERA_INDEX = 1


def get_auth(face, license_number) -> bool:
    data = {
        'face': face,
        'license_number': license_number
    }

    res = requests.post(MAIN_SERVER_REQUEST, data=jsonpickle.encode(data))
    print(res.content)
    if res.status_code != 200:
        raise ValueError

    return res.content == b'True'

def main():
    while True:
        face = take_face(FACE_CAMERA_INDEX)
        license_number = take_car_num()

        cv2.imwrite('face.jpg', face)

        try:
            is_auth = get_auth(face, license_number)
            if is_auth:
                gate_open()
            else:
                unauthorized()
        except Exception as e:
            print(e)
            unrecognized()


if __name__ == '__main__':
    main()
