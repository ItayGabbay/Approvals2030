from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .utils import *
import jsonpickle

@csrf_exempt
@require_POST
def add_entry_permit(request):
    print(jsonpickle.decode(request.body))
    return HttpResponse('raz')