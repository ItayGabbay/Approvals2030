# -*- coding: utf-8 -*-
from json import loads
from gate_controller import *
import os
import requests
import cv2
MAIN_SERVER_HOST = os.getenv('GATE_SERVICE_ADDR', 'http://127.0.0.1')
MAIN_SERVER_REQUEST = f'{MAIN_SERVER_HOST} + /getAuth'


def get_auth(face_img, car_img) -> bool:
    data = {
        'face': face_img,
        'car': car_img
    }

    res = requests.post(MAIN_SERVER_HOST, data=data)
    if res.status_code != 200:
        return False
    res_content = loads(res.content)
    return bool(res_content['auth'])



def main():
    while True:

        input('press to take face image')
        face = take_picture()
        cv2.imwrite('face.jpg', face)

        input('press to take car image')
        car = take_picture()
        cv2.imwrite('car.jpg', car)

        try:
            is_auth = get_auth(face, car)
            if is_auth:
                gate_open()
            else:
                unauthorized()
        except Exception as e:
            print(e)
            unrecognized()


if __name__ == '__main__':
    main()
