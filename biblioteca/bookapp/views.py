from django.shortcuts import redirect, render
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from bookapp.forms import *
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q


class UploadFormsView(LoginRequiredMixin, View):
    """
    Maneja y procesa los formularios que se le muestran al usuario
    """
    login_url = '/accounts/login/' # URL a la que redirecciona en caso no se tengan credenciales al acceder

    forms = {
        'fileForm': FileForm,
        'imageForm': ImageForm,
        'videoForm': VideoForm,
        'ytLinkForm': LinkForm,
        'carouselForm': CarouselForm,
        'categoryForm': CategoryForm,
        'metaKeywordForm': MetaKeywordForm
    }


    def get(self, request):
        return render(request, 'upload.html', self.forms)


    def post(self, request):
        form_name = self.forms[request.POST.get('name')]
        # Si el formulario lleva archivo
        if request.FILES: # Bastante mejorable no voy a mentir xd
            form = form_name(request.POST, request.FILES)
        # Si el formulario NO lleva archivo
        else:
            print(request.FILES, request.FILES == None)
            form = form_name(request.POST)

        # Valida el formulario
        if form.is_valid():
            form.save()
            messages.success(request, 'El formulario se ha enviado correctamente')
            return redirect('upload')
        else:
            # Muestra errores en el formulario
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])


class UpdateFormsView(LoginRequiredMixin, View):
    """
    Procesa la actualización de campos en objetos existentes
    """
    # URL a la que redirecciona en caso no se tengan credenciales al acceder
    login_url = '/accounts/login/'

    forms = {
        'file': FileForm,
        'image': ImageForm,
        'video': VideoForm,
        'link': LinkForm,
        'carousel': CarouselForm,
        'category': CategoryForm,
        'meta_keyword': MetaKeywordForm
    }

    models = {
        'file': File,
        'image': Image,
        'video': Video,
        'link': Link,
        'carousel': Carousel,
        'category': Category,
        'meta_keyword': MetaKeyword
    }

    def get(self, request, type, id):
        """ Manda el formulario rellenado según el id del contenido """
        context = {}
        context['media'] = self.models[type].objects.filter(id=id).first()
        context['form'] = self.forms[type](instance=context['media'])
        return render(request, 'update.html', context)


    def post(self, request, type, id):
        """ Recibe y procesa la actualización """
        form_name = self.forms[type]
        # Revisa si lleva archivos
        if request.FILES:
            form = form_name(request.POST, request.FILES, instance=self.models[type].objects.get(pk=id))
        # Si no lleva archivos
        else:
            form = form_name(request.POST, instance=self.models[type].objects.get(pk=id))
        
        # Valida el formulario
        if form.is_valid():
            form.save()
            messages.success(request, 'El formulario se ha actualizado correctamente')
            return redirect('home')
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])


class SearchResultsView(ListView):
    """
    Procesa y muestra los resultados de una busquéda
    """
    template_name = 'search.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        """
        Devuelve un diccionario con los resultados de la busqueda
        que son querysets de cada tipo de contenido
        """
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context.update({
            'query': query,
        })
        return context

    # Funcion que no se puede dejar vacia
    def get_queryset(self):
        query = self.request.GET.get('q')
        # BASTANTE REFACTORIZABLE, DEBERIA ARREGLAR ESTO PQ NO ESCALA MUY BIEN Y SE REPITE MUCHO
        kw_q = MetaKeyword.objects.filter(keyword__icontains=query)
        kw = []
        if kw_q:
            print(kw_q)
            for k in kw_q:
                kw.append(k.pk)
        objects = {
            'file': File.objects.filter(
                Q(title__icontains=query) | Q(author__icontains=query) | Q(keywords__in=kw)
                ),
            'video': Video.objects.filter(
                Q(title__icontains=query) | Q(author__icontains=query) | Q(keywords__in=kw)
            ),
            'image': Image.objects.filter(
                Q(title__icontains=query) | Q(author__icontains=query) | Q(keywords__in=kw)
            ),
            'link': Link.objects.filter(
                Q(title__icontains=query) | Q(author__icontains=query) | Q(keywords__in=kw)
            ),
        }
        queryset = []

        # Junta los objetos en una lista
        for key in objects:
            queryset += list(objects[key])

        return queryset
    

class CarouselListView(ListView):
    """
    Maneja la actualización y eliminación de imagenes que aparecen en el carrusel
    de la página de inicio. Retorna un diccionario 'object_list' al template
    'listview.html' que contiene las instancias del modelo
    """
    model = Carousel
    template_name = 'listview.html'

    # Sobreescribe le metodo para regresar un diccionario con las instancias de Carousel
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MetaKeywordsListView(ListView):
    """
    Maneja la actualización y eliminación de palabras clave
    Retorna un diccionario 'object_list' al template 'listview.html' que contiene las instancias
    del modelo
    """
    model = MetaKeyword
    template_name = 'listview.html'


class CategoryListView(ListView):
    """
    Maneja la actualización y eliminación de categorías
    Retorna un diccionario 'object_list' al template 'listview.html' que contiene las instancias
    del modelo
    """
    model = Category
    template_name = 'listview.html'


def home_view(request):
    """
    Vista para la página de inicio
    """
    context = {
        'files': File.objects.all(),
        'videos': Video.objects.all(),
        'images': Image.objects.all(),
        'links': Link.objects.all(),
    }

    # Indica el número de objetos por página
    paginate_by = 20

    # Lista los objetos para su paginacion
    object_list = []
    for key in context:
        object_list += list(context[key])

    # Pagina los objetos del contexto
    paginator = Paginator(object_list, paginate_by)
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', 
        {'page_obj': page_obj, 
        'carousel_img': Carousel.objects.all(),
        'categories': Category.objects.all()})


def home_view_filter(request, filter_by):
    """
    Vista para la página de inicio
    el argumento filter_by sirve para filtrar
    los objetos por categorías
    """
    context = {
        'files': File.objects.filter(category__exact=filter_by),
        'videos': Video.objects.filter(category__exact=filter_by),
        'images': Image.objects.filter(category__exact=filter_by),
        'links': Link.objects.filter(category__exact=filter_by),
    }

    # Indica el número de objetos por página
    paginate_by = 20

    # Lista los objetos para su paginacion
    object_list = []
    for key in context:
        object_list += list(context[key])

    # Pagina los objetos del contexto
    paginator = Paginator(object_list, paginate_by)
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', 
        {'page_obj': page_obj, 
        'carousel_img': Carousel.objects.all(),
        'categories': Category.objects.all()})


# BASTANTE REFACTORIZABLE NO VOY A MENTIR XDDD
def file_detail(request, type, id):
    models = {
        'file': File,
        'image': Image,
        'video': Video,
        'link': Link,
        'carousel': Carousel,
        'category': Category,
        'meta_keyword': MetaKeyword,
    }
    context = {}
    context['media'] = models[type].objects.get(pk=id)

    return render(request, 'content.html', context)


# PERO DIOS MIO ME QUIERO SACAR LOS OJOS COMO PUDE ESCRIBIR ESTO
@login_required(login_url='/accounts/login/')
def delete_file(request, type, id):
    models = {
        'file': File,
        'image': Image,
        'video': Video,
        'link': Link,
        'carousel': Carousel,
        'category': Category,
        'meta_keyword': MetaKeyword,
    }
    try:
        content_type = models[type].objects.get(pk=id)
    except content_type.DoesNotExist:
            messages.error(request,'El contenido que ha intentado eliminar no existe')
            return redirect('home')
    content_type.delete()
    messages.success(request, f'El contenido {content_type} ha sido eliminado exitosamente')
    return redirect('home')