# bookings/urls.py
from django.urls import path

from account import views

urlpatterns = [
    path("", views.simple_upload, name="simple_upload"),
    path("model_form_upload/", views.model_form_upload, name="simple_upload"),
]