from django.urls import path
from .views import *
from django.views.generic.base import TemplateView 

urlpatterns = [
    path('', homeView, name = 'home'),
    # URLs para visualizar el contenido
    path('file/<str:id>/', file_detail, name = 'detail'),
    path('video/<str:id>/', file_detail, name = 'detail'),
    path('image/<str:id>/', file_detail, name = 'detail'),
    path('link/<str:id>/', file_detail, name = 'detail'),
    # URLs para eliminar un contenido
    path('<str:type>/delete/<int:id>/', delete_file, name = 'delete'),
    # URL para subir contenido
    path('upload/', UploadFormsView.as_view(), name='upload')
    #path('upload/', views.image_form_view, name = 'upload')
    #path('', TemplateView.as_view(template_name='home.html'), name='home'),
]