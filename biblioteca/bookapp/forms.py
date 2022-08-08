from django import forms
from .models import *


class CategoryForm(forms.ModelForm):
    class Meta():
        model = Category
        fields = ('category',)


class MetaKeywordForm(forms.ModelForm):
    class Meta():
        model = MetaKeyword
        fields = ('keyword',)
        help_texts = {
            'keyword': '*Procura escribir con guiones y sin tildes. Ej: infografia-medio-ambiente',
        }


class FileForm(forms.ModelForm):
    class Meta():
        model = File
        fields = ('category', 'title', 'author', 'summary', 'file', 'cover', 'keywords')


class VideoForm(forms.ModelForm):
    class Meta():
        model = Video
        fields = ('category', 'title', 'author', 'summary', 'video', 'keywords')
        help_texts = {
            'author': '*Este campo es opcional',
        }


class ImageForm(forms.ModelForm):
    class Meta():
        model = Image
        fields = ('category', 'title', 'author', 'img', 'keywords')
        help_texts = {
            'author': '*Este campo es opcional',
        }


class LinkForm(forms.ModelForm):
    class Meta():
        model = Link
        fields = ('category', 'title', 'author', 'link', 'keywords')
        help_texts = {
            'author': 'Este campo es opcional',
            'link': 'Copia el link que aparece al dar click sobre compartir y luego insertar',
        }


class CarouselForm(forms.ModelForm):
    class Meta():
        model = Carousel
        fields = ('img',)
        help_texts = {
            'img': '*Procura que las imágenes sean del mismo tamaño',
        }