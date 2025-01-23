from django.urls import path

from soap_request import views

urlpatterns = [
    path('request', views.soap_request, name='soap_request'),
]