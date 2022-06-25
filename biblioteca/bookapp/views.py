from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.views.generic import View
from bookapp.forms import *
from .models import *
from django.contrib import messages


def homeView(request):
    context = {
        'files': File.objects.all(),
        'videos': Video.objects.all(),
        'images': Image.objects.all(),
        'links': Link.objects.all()
    }
    return render(request, 'home.html', context)


class UploadFormsView(View):
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
        if form_name == 'ytLinkForm':
            form = form_name(request.POST)
        # Si el formilario lleva archivo
        else:
            form_name = self.forms[request.POST.get('name')]
            form = form_name(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'El formulario se ha enviado correctamente')
            return redirect('upload')
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])