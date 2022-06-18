from django import forms
from .models import *

# Formulario para subir un Libro PDF
class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'keywords', 'publication_date', 'author', 'summary', 'cover', 'book_upload')


# Formulario para una imagen
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'keywords', 'publication_date', 'image_upload')


# Formulario para subir un video
class UploadVideoForm(forms.ModelForm):

    class Meta:
        model = Video
        fields = ('title', 'keywords', 'publication_date', 'author', 'summary', 'thumbnail')


# Formulario para subir un link de YouTube
class UploadYtLinkForm(forms.ModelForm):
    class Meta:
        model = YtLink
        fields = ('title', 'keywords', 'publication_date', 'link')