from django.urls import path

from . import views

urlpatterns = [
    path('AddEntryPermit', views.add_entry_permit, name='AddEntryPermit'),
    path('validatePerson', views.validate_erson, name='validatePerson'),    
]