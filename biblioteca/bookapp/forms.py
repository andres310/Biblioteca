"""
 - Autor: Andrés Alexander Meléndez Martínez
 - Creado el 30/04/2022
 - Proyecto de horas sociales en biblioteca
 - Este archivo contiene los formularios para los modelos,
 también las modificaciones pertienentes a estos, como los textos de ayuda,
 el elemento HTML que representa cada campo, el estilo aplicado, etc
 Para más información: https://docs.djangoproject.com/en/4.1/topics/forms/modelforms/
 https://docs.djangoproject.com/en/4.1/ref/forms/widgets/
"""

from django import forms
from .models import *


class CategoryForm(forms.ModelForm):
    class Meta():
        model = Category
        fields = '__all__'


class MetaKeywordForm(forms.ModelForm):
    class Meta():
        model = MetaKeyword
        fields = '__all__'
        help_texts = {
            'keyword': '*Procura escribir con guiones y sin tildes. Ej: infografia-medio-ambiente',
        }


class FileForm(forms.ModelForm):
    class Meta():
        model = File
        fields = ('category', 'title', 'author', 'summary', 'file', 'cover', 'keywords')
        widgets = {
            'keywords': forms.widgets.CheckboxSelectMultiple(),
        }


class VideoForm(forms.ModelForm):
    class Meta():
        model = Video
        fields = '__all__'
        help_texts = {
            'author': '*Este campo es opcional',
        }
        widgets = {
            'keywords': forms.widgets.CheckboxSelectMultiple(),
        }


class ImageForm(forms.ModelForm):
    class Meta():
        model = Image
        fields = '__all__'
        help_texts = {
            'author': '*Este campo es opcional',
        }
        widgets = {
            'keywords': forms.widgets.CheckboxSelectMultiple(),
        }


class LinkForm(forms.ModelForm):
    class Meta():
        model = Link
        fields = '__all__'
        help_texts = {
            'author': 'Este campo es opcional',
            'link': 'Copia el link que aparece al dar click sobre compartir y luego insertar',
        }
        widgets = {
            'keywords': forms.widgets.CheckboxSelectMultiple(),
        }


class CarouselForm(forms.ModelForm):
    class Meta():
        model = Carousel
        fields = '__all__'
        help_texts = {
            'img': '*Procura que las imágenes sean del mismo tamaño',
        }