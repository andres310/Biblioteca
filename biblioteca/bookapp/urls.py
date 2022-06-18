from django.urls import path
from bookapp import views
from django.views.generic.base import TemplateView 

urlpatterns = [
    path('', views.homeView, name = 'home'),
    #path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('upload/', views.UploadFormsView.as_view(), name = 'upload'),
    #path('upload/', views.uploadFileFormView, name = 'upload'),
    #path('upload/', views.uploadImageFormView, name = 'upload'),
    #path('upload/', views.uploadVideoFormView, name = 'upload'),
    #path('upload/', views.uploadYtLinkFormView, name = 'upload'),
]