from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import jsonpickle
import cv2
from random import getrandbits

from .models import Approvals
from .utils import *


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


@require_POST
def validate_erson(request):
    face = request.POST.get('face'),
    license_number = request.POST.get('license_number')

    try:
        person = Approvals.objects.get(license_number=license_number)
    except:
        return HttpResponse(False)
    return HttpResponse(True)
