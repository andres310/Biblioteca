from django.urls import path
from .views import *
from django.views.generic.base import TemplateView 

urlpatterns = [
    path('', homeView, name = 'home'),
    # URLs para visualizar el contenido
    path('<str:type>/<int:id>/', file_detail, name = 'detail'),
    # URLs para eliminar un contenido
    path('<str:type>/delete/<int:id>/', delete_file, name = 'delete'),
    # URL para actualizar un contenido
    path('<str:type>/update/<int:id>', UpdateFormsView.as_view(), name='update'),
    # URL para subir contenido
    path('upload/', UploadFormsView.as_view(), name='upload'),
    # URL para busqueda de contenido
    path('search/', SearchResultsView.as_view(), name='search')
]