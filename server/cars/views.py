from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .utils import *

import jsonpickle
from .models import Approvals


@csrf_exempt
@require_POST
def add_entry_permit(request):

    print(jsonpickle.decode(request.body))
    return HttpResponse('raz')


@require_POST
def validate_erson(request):
    face = request.POST.get('face'),
    license_number = request.POST.get('license_number')

    try:
        person = Approvals.objects.get(license_number=license_number)
    except:
        return HttpResponse(False)
    return HttpResponse(True)
