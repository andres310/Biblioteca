from django.db import models

# Interfaz de Archivo
class File(models.Model):
    title = models.CharField('Titulo', max_length=255)
    keywords = models.CharField('Palabras clave', max_length=255)
    publication_date = models.DateField('Fecha de publicacion')
    #file = models.FileField()
    #url = models.URLField()


# Libros en formato PDF. hereda de File
class Book(File):
    author = models.CharField('Autor', max_length=255)
    summary = models.TextField('Descripcion')
    cover = models.ImageField()
    book_upload = models.FileField(default='')


# Imagenes, hereda de File
class Image(File):
    image_upload = models.ImageField()


# Videos
class Video(File):
    author = models.CharField('Autor', max_length=255)
    summary = models.TextField('Descripcion')
    thumbnail = models.ImageField(upload_to='uploads/% y/% m/% d')


# Links de youtube
class YtLink(File):
    link = models.URLField()