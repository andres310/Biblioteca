from django.shortcuts import render

from .forms import CustomUserCreationForm
from . import models
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView


class SignUpView(CreateView):
    """
    Crea una vista para el registro de usuarios usando las modificaciones seguras de CustomUser
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

