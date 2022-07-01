from re import A
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.views.generic import View
from bookapp.forms import *
from .models import *
from django.contrib import messages


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


class ContentDispatchView(View):
    """
    Procesa las urls para el detalle de un contenido, brindando la página de ese contenido
    """


    def get(self, request):
        content_type = request.get_full_path().split('/')[1]
        context = {'content': content_type}
        return render(request, 'content.html', context)


def homeView(request):
    context = {
        'files': File.objects.all(),
        'videos': Video.objects.all(),
        'images': Image.objects.all(),
        'links': Link.objects.all()
    }
    return render(request, 'home.html', context)


def file_detail(request, id):
    content_type = request.get_full_path()
    context = {}
    if 'file' in content_type:
        context['media'] = File.objects.get(pk=id)
        context['is_file'] = True
    elif 'video' in content_type:
        context['media'] = Video.objects.get(pk=id)
        context['is_video'] = True
    elif 'image' in content_type:
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