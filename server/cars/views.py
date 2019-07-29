from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .utils import *

@require_POST
def add_entry_permit(request):
    return HttpResponse('raz')