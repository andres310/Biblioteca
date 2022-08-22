"""
 - Autor: Andrés Alexander Meléndez Martínez
 - Creado el 30/04/2022
 - Proyecto de horas sociales en biblioteca
 - Este archivo contiene las URLs que usan las vistas (views.py) 
 de bookapp (solo de este módulo) para cargar en el navegador
"""

from django.urls import path
from .views import *
from django.views.generic.base import TemplateView 

urlpatterns = [
    # URL para mostrar la página de inicio
    path('', home_view, name = 'home'),
    # URLs para filtrar por categoria la página de inicio
    path('<int:filter_by>', home_view_filter, name = 'home_filter'),
    # URLs para visualizar el contenido
    path('<str:type>/<int:id>/', file_detail, name = 'detail'),
    # URLs para eliminar un contenido
    path('<str:type>/delete/<int:id>/', delete_file, name = 'delete'),
    # URL para actualizar un contenido
    path('<str:type>/update/<int:id>', UpdateFormsView.as_view(), name='update'),
    # URL para subir contenido
    path('upload/', UploadFormsView.as_view(), name='upload'),
    # URL para busqueda de contenido
    path('search/', SearchResultsView.as_view(), name='search'),
    # URL para editar y eliminar imagenes del carrusel
    path('carousel/', CarouselListView.as_view(), name='carousel'),
    # URL para editar y eliminar categorías
    path('categories/', CategoryListView.as_view(), name='categories'),
    # URL para editar y eliminar palabras clave
    path('keywords/', MetaKeywordsListView.as_view(), name='keywords'),
]