from django.urls import path
from .views import *
from django.views.generic.base import TemplateView 

urlpatterns = [
    path('', homeView, name = 'home'),
    path('upload/', UploadFormsView.as_view(), name='upload')
    #path('upload/', views.image_form_view, name = 'upload')
    #path('', TemplateView.as_view(template_name='home.html'), name='home'),
]