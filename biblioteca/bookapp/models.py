from django.db import models


class File(models.Model):
    title = models.CharField(verbose_name='Título', max_length=255, null=False)
    author = models.CharField(verbose_name='Autor', max_length=255, null=False)
    summary = models.TextField(verbose_name='Descripción', null=False)
    file = models.FileField(verbose_name='Archivo', upload_to='archivos/%y/%m/%d', null=False)
    cover = models.ImageField(verbose_name='Portada', upload_to='portadas/%y/%m/%d', null=True)
    publication_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    class Meta():
        db_table = 'files'
        verbose_name = 'Archivo'
        verbose_name_plural = 'Archivos'
        ordering = ['id']


class Video(models.Model):
    title = models.CharField(verbose_name='Título', max_length=255, null=False)
    author = models.CharField(verbose_name='Autor', max_length=255, null=False)
    summary = models.TextField(verbose_name='Descripción', null=True)
    video = models.FileField(verbose_name='Video', upload_to='videos/%y/%m/%d', null=False)

    def __str__(self) -> str:
        return self.video
    
    class Meta():
        db_table = 'videos'
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
        ordering = ['id']


class Image(models.Model):
    title = models.CharField(verbose_name='Título', max_length=255, null=False)
    img = models.ImageField(verbose_name='Imagen', upload_to='imagenes/%y/%m/%d', null=False)

    def __str__(self) -> str:
        return self.img
    
    class Meta():
        db_table = 'images'
        verbose_name = 'Imagen'
        verbose_name_plural = 'Imagenes'
        ordering = ['id']


class Link(models.Model):
    title = models.CharField(verbose_name='Título', max_length=255, null=False)
    link = models.URLField(verbose_name='Link', null=False)

    def __str__(self) -> str:
        return self.link

    class Meta():
        db_table = 'links'
        verbose_name = 'Link'
        verbose_name_plural = 'Links'
        ordering = ['id']