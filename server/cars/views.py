from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
import jsonpickle
import cv2
import numpy as np
from random import getrandbits

from .utils import *
from .models import Approvals
from cv2 import imread
import requests

FACE_SERVER_HOST = 'http://face-recognition.westeurope.cloudapp.azure.com:8080/predict'

@csrf_exempt
def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render({}, request))

@csrf_exempt
@require_POST
def add_entry_permit(request):
    data = jsonpickle.decode(request.body)
    img = extract_face(data['photo'])
    if img is None:
        raise Http404

    filename =  os.path.join('static', 'images', 'face-{}-{}.jpeg'.format(data['user']['first_name'], str(getrandbits(20))))
    cv2.imwrite(filename, img)
    candidate = Approvals(name=data['user']['first_name'],
                          license_number=data['plate'],
                          description=data['description'],
                          picture=filename,
                          is_authorized=False)
    candidate.save()
    return HttpResponse('200')

@csrf_exempt
@require_POST
def validate_person(request):
    body = decode_body(request)
    face = np.array(body.get('face'))
    license_number = body.get('license_number')

    try:
        persons = Approvals.objects.filter(is_authorized=True)
    except:
        return HttpResponse(False)    

    all_faces = [imread(os.path.dirname(__file__) + '\\p.picture') for p in persons]

    data= {
        'face': face,
        'all_faces': all_faces
    }
    res = requests.post(FACE_SERVER_HOST, data=jsonpickle.dumps(data))
    if res.status_code != 200:
        return HttpResponse(False)
    predictions = jsonpickle.loads(res.content)

    if sum(predictions) == 0:
        return HttpResponse(False)

    elif sum(predictions) != 1:
        raise Http404

    if license_number != '':
        index = predictions.index(True)
        if persons[index].license_number == license:
            return HttpResponse(True)
        return HttpResponse(False)
    else:
        return HttpResponse(True)

    return HttpResponse(False)

@csrf_exempt
def get_all_persons(request):
    return HttpResponse(jsonpickle.encode(list(Approvals.objects.all()), unpicklable=False))


@csrf_exempt
def update_approval(request):
    id = request.GET.get('id')
    is_authorized = request.GET.get('is_authorized') == 'true'

    appr = Approvals.objects.get(id=id)
    appr.is_authorized = is_authorized
    appr.save()
    BOT_API_KEY = '951740858:AAHDXXwE0dYA3UTXQnetnPq5D2FWlWqKqw4'
    MY_CHANNEL_NAME = appr.chat_id
    if is_authorized:
        MY_MESSAGE_TEXT = 'You are authorized now!'
        requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s' % (BOT_API_KEY, MY_CHANNEL_NAME, MY_MESSAGE_TEXT))
    else:
        MY_MESSAGE_TEXT = 'Sorry, You are not authorized'
        requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s' % (BOT_API_KEY, MY_CHANNEL_NAME, MY_MESSAGE_TEXT))
    return HttpResponse(200)