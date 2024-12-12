from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime


class BibliotecaModelForm(ModelForm):
    class meta:
        fields = ['nombre', 'direccion']
        