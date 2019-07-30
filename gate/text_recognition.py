# USAGE
# python text_recognition.py --east frozen_east_text_detection.pb --image images/example_01.jpg
# python text_recognition.py --east frozen_east_text_detection.pb --image images/example_04.jpg --padding 0.05
import cv2
import Plate_getter
import requests
import json
import re

OCR_API_KEY = '6db9fed6d988957'


def search_plates(image):
    plates = Plate_getter.get_plate(image)
    if not plates:
        return None
    ret_plates = []
    for i, plate in enumerate(plates):
        payload = {
            'apikey': OCR_API_KEY,
            'language': 'eng'
        }
        is_success, buffer = cv2.imencode(".jpeg", plate)
        if is_success:
            res = requests.post(
                'https://api.ocr.space/parse/image',
                files={f'plate-{i}.jpeg': buffer},
                data=payload,
            )
            if res.status_code == 200:
                data = json.loads(res.content)['ParsedResults'][0]['ParsedText']
                data = ''.join(list(filter(lambda x: x.isdigit(), data)))
                if len(data) in [7, 8]:
                    ret_plates.append(data)
            elif res.status_code == 403:
                print('replace ocr token', res.content)
                return False
    if len(ret_plates) == 0:
        return  None
    return ret_plates[0]
