from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from bookapp.forms import *
from .functions import handle_uploaded_file
from django.forms import ModelForm


def homeView(request):
    files = File.objects.all()
    return render(request, 'home.html', {'files': files})


class UploadFormsView(View):
    def get(self, request):
        forms = {
            'fileForm': UploadFileForm(),
            'imageForm': UploadImageForm(),
            'videoForm': UploadVideoForm(),
            'ytLinkForm': UploadYtLinkForm()
        }
        return render(request, 'upload.html', forms)


    def post(self, request):
        form = UploadImageForm(data=request.POST, files=request.FILES) # esto da problemas
        if form.is_valid():
            form.save()
            return HttpResponse('Funciona :D!')


def uploadFileFormView(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            form.save()
            return HttpResponse('Funciona :D!')
    else:
        form = UploadFileForm()
        return render(request, 'upload.html', {'fileForm': form})


def uploadImageFormView(request):
    if request.method == 'POST':
        imageForm = UploadImageForm(data=request.POST, files=request.FILES) # AQUI ESTA EL PROBLEMA
        if imageForm.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            imageForm.save()
            return HttpResponse('Funciona :D!')
    else:
        imageForm = UploadImageForm()
        return render(request, 'upload.html', {'imageForm': imageForm})


def uploadVideoFormView(request):
    if request.method == 'POST':
        form = UploadVideoForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse('Funciona :D!')
    else:
        form = UploadVideoForm()
        return render(request, 'upload.html', {'videoForm': form})


def uploadYtLinkFormView(request):
    if request.method == 'POST':
        form = UploadYtLinkForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse('Funciona :D!')
    else:
        form = UploadYtLinkForm()
        return render(request, 'upload.html', {'ytLinkForm': form})