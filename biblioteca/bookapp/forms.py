from django import forms
from .models import *


class FileForm(forms.ModelForm):
    class Meta():
        model = File
        fields = ('title', 'author', 'summary', 'file', 'cover')


class VideoForm(forms.ModelForm):
    class Meta():
        model = Video
        fields = ('title', 'author', 'summary', 'video')


class ImageForm(forms.ModelForm):
    class Meta():
        model = Image
        fields = ('title', 'img')


class LinkForm(forms.ModelForm):
    class Meta():
        model = Link
        fields = ('title', 'link')