from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [

    path('signup/', views.SignUpView.as_view(), name='signup')
]