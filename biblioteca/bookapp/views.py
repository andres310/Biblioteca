from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.views.generic import View, ListView
from bookapp.forms import *
from .models import *
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator


class UploadFormsView(View):
    """
    Maneja y procesa los formularios que se le muestran al usuario
    """
    forms = {
        'fileForm': FileForm,
        'imageForm': ImageForm,
        'videoForm': VideoForm,
        'ytLinkForm': LinkForm
    }


    def get(self, request):
        return render(request, 'upload.html', self.forms)


    def post(self, request):
        form_name = self.forms[request.POST.get('name')]
        # Si el formulario no lleva archivo
        if form_name == 'ytLinkForm': # Bastante mejorable no voy a mentir xd
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


class UpdateFormsView(View):
    """
    Procesa la actualización de campos en objetos existentes
    """
    forms = {
        'file': FileForm,
        'image': ImageForm,
        'video': VideoForm,
        'link': LinkForm
    }


    def get(self, request, type, id):
        """ Manda el formulario rellenado según el id del contenido """
        context = {}
        if 'file' in type:
            context['media'] = File.objects.filter(id=id).first()
            context['form'] = FileForm(instance=context['media'])
        elif 'video' in type:
            context['media'] = Video.objects.filter(id=id).first()
            context['form'] = VideoForm(instance=context['media'])
        elif 'image' in type:
            context['media'] = Image.objects.filter(id=id).first()
            context['form'] = ImageForm(instance=context['media'])
        else:
            context['media'] = Link.objects.filter(id=id).first()
            context['form'] = LinkForm(instance=context['media'])
        
        return render(request, 'update.html', context)


    def post(self, request, type, id):
        """ Recibe y procesa la actualización """
        form_name = self.forms[type]
        if 'link' in type:
            form = form_name(request.POST, instance=Link.objects.get(pk=id))
        elif 'file' in type:
            form = form_name(request.POST, request.FILES, instance=File.objects.get(pk=id))
        elif 'video' in type:
            form = form_name(request.POST, request.FILES, instance=Video.objects.get(pk=id))
        else:
            form = form_name(request.POST, request.FILES, instance=Image.objects.get(pk=id))

        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])


class SearchResultsView(ListView):
    models = [File, Video, Image, Link]
    template_name = 'search.html'


    def get_queryset(self):
        query = self.request.GET.get('q')
        file_list = File.objects.filter(title__icontains=query).values('title', 'cover')
        video_list = Video.objects.filter(title__icontains=query).values('title', 'video')
        image_list = Image.objects.filter(title__icontains=query).values('title', 'img')
        link_list = Link.objects.filter(Q(title__icontains=query)).values('title', 'link')
        object_list = file_list.union(video_list).union(image_list).union(link_list)
        print(object_list)
        return object_list


def homeView(request):
    context = {
        'files': File.objects.all(),
        'videos': Video.objects.all(),
        'images': Image.objects.all(),
        'links': Link.objects.all()
    }
    return render(request, 'home.html', context)


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


def delete_file(request, type, id):
    try:
        content_type = type
        if 'file' in content_type:
            content_type = File.objects.get(pk=id)
        elif 'video' in content_type:
            content_type = Video.objects.get(pk=id)
        elif 'image' in content_type:
            content_type = Image.objects.get(pk=id)
        else:
            content_type = Link.objects.get(pk=id)
    except content_type.DoesNotExist:
            messages.error(request,'El contenido que ha intentado eliminar no existe')
            return redirect('home')
    content_type.delete()
    messages.success(request, f'El contenido {content_type} ha sido eliminado exitosamente')
    return redirect('home')