"""
 - Autor: Andrés Alexander Meléndez Martínez
 - Creado el 30/04/2022
 - Proyecto de horas sociales en biblioteca
 - Este archivo contiene las funciones que validan las extensiones
 de los archivos subidos, estas funciones están implementadas en
 models.py (de éste módulo) en el atributo correspondiente a cada archivo en
 el modelo se encuentra un argumento 'validators=' en la función que crea el campo
 en la base de datos
"""

import os
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    """
    Función que valida las extemsiones permitidas para los archivos las cuales son:
    .pdf, .docx, .xslx, .xslm, .xslb, .xltx
    """
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.docx', '.xslx', '.xslm', '.xlsb', '.xltx']
    if not extension in valid_extensions:
        raise ValidationError(u'Tipo de archivo no soportado!')


def validate_image_extension(value):
    """
    Función que valida las extensiones permitidas para las imagenes las cuales son:
    .png, .jpg y .jpeg
    """
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not extension in valid_extensions:
        raise ValidationError(u'Tipo de imagen no soportada!')


def validate_video_extension(value):
    """
    Función que valida las extensiones permitidas para videos las cuales son:
    .mp4 y .webm
    """
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp4', '.webm']
    if not extension in valid_extensions:
        raise ValidationError(u'Tipo de video no soportado!')