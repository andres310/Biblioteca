from unicodedata import category
from .validators import *
from django.db import models
from django.template.defaultfilters import slugify
import os


class Category(models.Model):
    """
    Representación de la tabla Category en la base de datos
    """
    category = models.CharField(verbose_name='Categoría', max_length=255, null=False)

    def __str__(self) -> str:
        return self.category

    # Devuelve el tipo de multimedia como string para su identificacion
    def content_type(self):
        return 'category'

    class Meta():
        db_table = 'categories'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']


class MetaKeyword(models.Model):
    """
    Representación de la tabla meta_keywords en la base de datos
    Contiene las palabras claves (tags) para se usados por las
    demás tablas
    """
    keyword = models.CharField(verbose_name='Palabra clave', max_length=255, null=False)

    def __str__(self) -> str:
        return self.keyword

    # Devuelve el tipo de multimedia como string para su identificacion
    def content_type(self):
        return 'meta_keyword'

    class Meta():
        db_table = 'meta_keywords'
        verbose_name = 'Palabra_clave'
        verbose_name_plural = 'Palabras_clave'
        ordering = ['id']


class File(models.Model):
    """
    Representación de la tabla File en la base de datos
    """
    # Llave foranea
    category = models.ForeignKey('Category', verbose_name='Categoría', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Título', max_length=255, null=False)
    author = models.CharField(verbose_name='Autor', max_length=255, null=False)
    summary = models.TextField(verbose_name='Descripción', null=False)
    file = models.FileField(verbose_name='Archivo', upload_to='archivos/%y/%m/%d', validators=[validate_file_extension], null=False)
    cover = models.ImageField(verbose_name='Portada', upload_to='portadas/%y/%m/%d', validators=[validate_image_extension], null=True)
    keywords = models.ManyToManyField(MetaKeyword, verbose_name='Palabras clave')
    publication_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return slugify(self.title)

    # Sobreescribe el metodo delete para eliminar el contenido multimedia
    def delete(self, *args, **kwargs):
        # Elimina la portada del archivo
        if os.path.isfile(self.cover.path):
            os.remove(self.cover.path)
        # Elimina el archivo
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)
        # Llama a la funcion que sobreescribe para continuar normalmente
        super(File, self).delete(*args, **kwargs)

    # Devuelve el tipo de multimedia como string para su identificacion
    def content_type(self):
        return 'file'

    class Meta():
        db_table = 'files'
        verbose_name = 'Archivo'
        verbose_name_plural = 'Archivos'
        ordering = ['id']


class Video(models.Model):
    """
    Representación de la tabla Video en la base de datos
    """
    # Llave foranea
    category = models.ForeignKey('Category', verbose_name='Categoría', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Título', max_length=255, null=False)
    author = models.CharField(verbose_name='Autor', max_length=255, null=False)
    summary = models.TextField(verbose_name='Descripción', null=True)
    video = models.FileField(verbose_name='Video', upload_to='videos/%y/%m/%d', validators=[validate_video_extension], null=False)
    keywords = models.ManyToManyField(MetaKeyword,  verbose_name='Palabras clave')

    def __str__(self) -> str:
        return slugify(self.title)

    # Sobreescribe el metodo delete para eliminar el contenido multimedia
    def delete(self, *args, **kwargs):
        # Elimina el video
        if os.path.isfile(self.video.path):
            os.remove(self.video.path)
        # Llama a la funcion que sobreescribe para continuar normalmente
        super(Video, self).delete(*args, **kwargs)

    # Devuelve el tipo de multimedia como string para su identificacion
    def content_type(self):
        return 'video'
    
    class Meta():
        db_table = 'videos'
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
        ordering = ['id']


class Image(models.Model):
    """
    Representación de la tabla Image en la base de datos
    """
    # Llave foranea
    category = models.ForeignKey('Category', verbose_name='Categoría', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Título', max_length=255, null=False)
    author = models.CharField(verbose_name='Autor', max_length=255, null=True, blank=True)
    img = models.ImageField(verbose_name='Imagen', upload_to='imagenes/%y/%m/%d', validators=[validate_image_extension], null=False)
    keywords = models.ManyToManyField(MetaKeyword, verbose_name='Palabras clave')

    def __str__(self) -> str:
        return slugify(self.title)

    # Sobreescribe le metodo delete para eliminar el contenido multimedia
    def delete(self, *args, **kwargs):
        # Elimina la imagen
        if os.path.isfile(self.img.path):
            os.remove(self.img.path)
        # Llama a la funcion que sobreescribe para continuar normalmente
        super(Image, self).delete(*args, **kwargs)

    # Devuelve el tipo de multimedia como string para su identificacion
    def content_type(self):
        return 'image'
    
    class Meta():
        db_table = 'images'
        verbose_name = 'Imagen'
        verbose_name_plural = 'Imagenes'
        ordering = ['id']


class Link(models.Model):
    """
    Representación de la tabla Link en la base de datos
    """
    # Llave foranea
    category = models.ForeignKey('Category', verbose_name='Categoría', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Título', max_length=255, null=False)
    author = models.CharField(verbose_name='Autor', max_length=255, null=True, blank=True)
    link = models.URLField(verbose_name='Link', null=False)
    keywords = models.ManyToManyField(MetaKeyword, verbose_name='Palabras clave')

    def __str__(self) -> str:
        return slugify(self.title)

    # Devuelve el tipo de multimedia como string para su identificacion
    def content_type(self):
        return 'link'

    class Meta():
        db_table = 'links'
        verbose_name = 'Link'
        verbose_name_plural = 'Links'
        ordering = ['id']


class Carousel(models.Model):
    """
    Representación de la tabla carrousel en la base de datos,
    maneja el uso del carrusel que se presenta en la página de inicio 'home'
    """
    img = models.ImageField(verbose_name='Imagen', upload_to='carrusel/', validators=[validate_image_extension], null=False)

    def content_type(self):
        return 'carousel'

    # Sobreescribe le metodo delete para eliminar el contenido multimedia
    def delete(self, *args, **kwargs):
        # Elimina la imagen
        if os.path.isfile(self.img.path):
            os.remove(self.img.path)
        # Llama a la funcion que sobreescribe para continuar normalmente
        super(Carousel, self).delete(*args, **kwargs)

    class Meta():
        db_table = 'carousel'
        verbose_name = 'Carousel'
        verbose_name_plural = 'Carousel'
        ordering = ['id']
