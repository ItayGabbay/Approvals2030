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

FACE_SERVER_HOST = 'http://10.104.238.17/predict'

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

    filename =  os.path.join(os.path.dirname(__file__), 'static', 'images', 'face-{}-{}.jpeg'.format(data['user']['first_name'], str(getrandbits(20))))
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
        persons = Approvals.objects.filter(is_authorized=False)
    except:
        return HttpResponse(False)    

    all_faces = [imread(p.picture) for p in persons]

    data= {
        'face': face,
        'all_faces': all_faces
    }
    res = requests.post(FACE_SERVER_HOST, data=jsonpickle.dumps(data))
    if res.status_code != 200:
        return HttpResponse(False)
    predictions = jsonpickle.loads(res.content)
    print(predictions, sum(predictions))
    if sum(predictions) == 0:
        return HttpResponse(False)

    elif sum(predictions) != 1:
        raise Http404
    else:
        return HttpResponse(True)
    # Else - sum == 1:

    try:
        index = predictions.index(True)
    except AttributeError:
        return HttpResponse(False)

    if persons[index].license_number == license:
        return HttpResponse(True)

    return HttpResponse(False)

@csrf_exempt
def get_all_perssons(request):
    return HttpResponse(jsonpickle.encode(list(Approvals.objects.all()), unpicklable=False))