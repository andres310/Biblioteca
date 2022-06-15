from django.shortcuts import render
from django.http import HttpResponse
from bookapp.functions import handle_uploaded_file
from bookapp.forms import UploadFileForm, UploadImageForm, UploadVideoForm


def upload(request):
    if request.method == 'POST':  
        file = UploadFileForm(request.POST, request.FILES)  
        if file.is_valid():  
            handle_uploaded_file(request.FILES['file_upload'])  
            return HttpResponse("File uploaded successfuly")  
    else:  
        file = UploadFileForm()  
        return render(request,"upload.html",{'form':UploadFileForm})
