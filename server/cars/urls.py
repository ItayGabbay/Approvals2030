from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('/AddEntryPermit', views.add_entry_permit, name='AddEntryPermit'),
]