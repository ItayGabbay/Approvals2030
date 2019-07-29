from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import jsonpickle
from .models import Approvals

from .utils import *

@csrf_exempt
@require_POST
def add_entry_permit(request):
    data = jsonpickle.decode(request.body)
    img = extract_face(data['photo'])

    candidate = Approvals(name=data['user'],
                  license_number=data['plate'],
                  description=data['description'],
                  picture=img,
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
