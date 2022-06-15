from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls'))
]