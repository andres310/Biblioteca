from django import forms


# Formulario para subir un Libro PDF
class UploadFileForm(forms.Form):
    title = forms.CharField(label='Titulo')
    author = forms.CharField(label='Autor')
    summary = forms.Textarea()
    keywords = forms.CharField(label='Palabras Clave')
    publication_date = forms.DateField(label='Fecha de publicación')
    cover = forms.ImageField(label='Portada') 
    file_upload = forms.FileField()


# Formulario para una imagen
class UploadImageForm(forms.Form):
    title = forms.CharField(label='Titulo')
    keywords = forms.CharField(label='Palabras Clave')
    publication_date = forms.DateField(label='Fecha de publicación')
    image = forms.ImageField()


# Formulario para subir un video
class UploadVideoForm(forms.Form):
    title = forms.CharField(label='Titulo')
    author = forms.CharField(label='Autor')
    summary = forms.Textarea()
    keywords = forms.CharField(label='Palabras Clave')
    publication_date = forms.DateField(label='Fecha de publicación')
    thumbnail = forms.ImageField(label='Miniatura')
    video = forms.FileField()