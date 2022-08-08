import re
from django.shortcuts import redirect, render
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from bookapp.forms import *
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


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
        # Si el formulario no lleva archivo
        if request.FILES: # Bastante mejorable no voy a mentir xd
            print(request.FILES, request.FILES == None)
            form = form_name(request.POST)
        # Si el formilario lleva archivo
        else:
            form_name = self.forms[request.POST.get('name')]
            form = form_name(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'El formulario se ha enviado correctamente')# quiza no se ve pq redirecciona muy rapido xd
            return redirect('upload')
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])


class UpdateFormsView(LoginRequiredMixin, View):
    """
    Procesa la actualización de campos en objetos existentes
    """
    login_url = '/accounts/login/' # URL a la que redirecciona en caso no se tengan credenciales al acceder

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

    """
    POR EL AMOR DE CRISTO HAY QUE REFACTORIZAR ESTO ANTES DE QUE ALGUIEN SALGA HERIDO
    """

    def get(self, request, type, id):
        """ Manda el formulario rellenado según el id del contenido """
        context = {}
        context['media'] = self.models[type].objects.filter(id=id).first()
        context['form'] = self.forms[type](instance=context['media'])
        """
        if 'file' in type:
            context['media'] = File.objects.filter(id=id).first()
            context['form'] = FileForm(instance=context['media'])
        elif 'video' in type:
            context['media'] = Video.objects.filter(id=id).first()
            context['form'] = VideoForm(instance=context['media'])
        elif 'image' in type:
            context['media'] = Image.objects.filter(id=id).first()
            context['form'] = ImageForm(instance=context['media'])
        elif 'carousel' in type:
            context['media'] = Carousel.objects.filter(id=id).first()
            context['form'] = CarouselForm(instance=context['media'])
        else:
            context['media'] = Link.objects.filter(id=id).first()
            context['form'] = LinkForm(instance=context['media'])
        """
        return render(request, 'update.html', context)


    def post(self, request, type, id):
        """ Recibe y procesa la actualización """
        form_name = self.forms[type]
        if request.FILES:
            form = form_name(request.POST, request.FILES, instance=self.models[type].objects.get(pk=id))
        else:
            form = form_name(request.POST, instance=self.models[type].objects.get(pk=id))
        """
        if 'link' in type:
            form = form_name(request.POST, instance=Link.objects.get(pk=id))
        elif 'file' in type:
            form = form_name(request.POST, request.FILES, instance=File.objects.get(pk=id))
        elif 'video' in type:
            form = form_name(request.POST, request.FILES, instance=Video.objects.get(pk=id))
        elif 'carousel' in type:
            form = form_name(request.POST, request.FILES, instance=Carousel.objects.get(pk=id))
        else:
            form = form_name(request.POST, request.FILES, instance=Image.objects.get(pk=id))
        """
        if form.is_valid():
            form.save()
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
        objects = {
            'file': File.objects.filter(title__icontains=query),
            'video': Video.objects.filter(title__icontains=query),
            'image': Image.objects.filter(title__icontains=query),
            'link': Link.objects.filter(title__icontains=query),
        }
        queryset = []
        # Junta los objetos en una lista
        for key in objects:
            queryset += list(objects[key])
        if 'search' in self.request.get_full_path():
            print(self.request.get_full_path())
            print(self.request.path)
        return queryset
    


class CarouselListView(ListView):
    """
    Maneja la creación, actualización y eliminación de imagenes que aparecen en el carrusel
    de la página de inicio
    """
    model = Carousel
    template_name = 'carousel.html'

    # Sobreescribe le metodo para regresar un diccionario con las instancias de Carousel
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def homeView(request):
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

    return render(request, 'home.html', {'page_obj': page_obj, 'carousel_img': Carousel.objects.all()})


# BASTANTE REFACTORIZABLE NO VOY A MENTIR XDDD
def file_detail(request, type, id):
    context = {}
    if 'file' in type:
        context['media'] = File.objects.get(pk=id)
        context['is_file'] = True
    elif 'video' in type:
        context['media'] = Video.objects.get(pk=id)
        context['is_video'] = True
    elif 'image' in type:
        context['media'] = Image.objects.get(pk=id)
        context['is_image'] = True
    else:
        context['media'] = Link.objects.get(pk=id)
        context['is_link'] = True
    return render(request, 'content.html', context)


# PERO DIOS MIO ME QUIERO SACAR LOS OJOS COMO PUDE ESCRIBIR ESTO
@login_required(login_url='/accounts/login/')
def delete_file(request, type, id):
    try:
        if 'file' in type:
            content_type = File.objects.get(pk=id)
        elif 'video' in type:
            content_type = Video.objects.get(pk=id)
        elif 'image' in type:
            content_type = Image.objects.get(pk=id)
        elif 'carousel' in type:
            content_type = Carousel.objects.get(pk=id)
        else:
            content_type = Link.objects.get(pk=id)
    except content_type.DoesNotExist:
            messages.error(request,'El contenido que ha intentado eliminar no existe')
            return redirect('home')
    content_type.delete()
    messages.success(request, f'El contenido {content_type} ha sido eliminado exitosamente')
    return redirect('home')