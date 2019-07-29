# -*- coding: utf-8 -*-
from json import loads
from gate.gate_controller import *
import os
import requests
import cv2

MAIN_SERVER_HOST = os.getenv('GATE_SERVICE_ADDR', 'http://127.0.0.1')
MAIN_SERVER_REQUEST = f'{MAIN_SERVER_HOST} + /getAuth'
FACE_CAMERA_INDEX = 0
CAR_CAMERA_INDEX = 1

def get_auth(face_img, car_num) -> bool:
    data = {
        'face': face_img,
        'car_num': car_num
    }

    res = requests.post(MAIN_SERVER_HOST, data=data)
    if res.status_code != 200:
        return False
    res_content = loads(res.content)
    return bool(res_content['auth'])

def main():
    while True:
        face_img = take_face()
        car_num = take_car_num()

        #TODO: not on prod
        cv2.imwrite('face.jpg', face_img)
        print(car_num)

        try:
            is_auth = get_auth(face_img, car_num)
            if is_auth:
                gate_open()
            else:
                unauthorized()
        except Exception as e:
            print(e)
            unrecognized()


if __name__ == '__main__':
    main()