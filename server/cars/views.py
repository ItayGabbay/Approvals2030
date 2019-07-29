from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .utils import *
from .models import Approvals

import numpy as np
from .models import Approvals


@csrf_exempt
@require_POST
def add_entry_permit(request):

    print(decode_body(request))
    return HttpResponse('raz')


@require_POST
def validate_person(request):
    body = decode_body(request)
    face = np.array(body.POST.get('face'))
    license_number = body.POST.get('license_number')

    try:
        person = Approvals.objects.filter(license_number=license_number, is_authorized=True).values('picture')
    except:
        return HttpResponse(False)    


    return HttpResponse(True)
