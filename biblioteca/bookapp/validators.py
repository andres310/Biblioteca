import os
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    """
    Función que valida las extemsiones permitidas para los archivos
    """
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.docx', '.xslx', '.xslm', '.xlsb', '.xltx']
    if not extension in valid_extensions:
        raise ValidationError(u'Tipo de archivo no soportado!')


def validate_image_extension(value):
    """
    Función que valida las extensiones permitidas para las imagenes
    """
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not extension in valid_extensions:
        raise ValidationError(u'Tipo de imagen no soportada!')


def validate_video_extension(value):
    """
    Función que valida las extensiones permitidas para videos
    """
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp4', '.webm']
    if not extension in valid_extensions:
        raise ValidationError(u'Tipo de video no soportado!')