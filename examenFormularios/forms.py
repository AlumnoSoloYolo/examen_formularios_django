from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime



class PromocionModelForm(ModelForm):
    class Meta:
        model = Promocion
        fields = ['nombre', 'descripcion', 'activa', 'descuento', 'inicio_promo', 'fin_promo', 'producto', 'usuarios']
        help_texts = {
            'descripcion': 'La descripción debe tener al menos 100 caracteres',
            'descuento': 'Debe ser un valor entre 0 y 10',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la promocion'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe aquí tu descripción...',
                'rows': 4,
                'cols': 50
            }),
            "inicio_promo": forms.DateInput(format="%Y-%m-%d", attrs={
                "class": "form-control",
                "type": "date"
            }),
            "fin_promo": forms.DateInput(format="%Y-%m-%d", attrs={
                "class": "form-control",
                "type": "date"
            }),
            "usuarios": forms.CheckboxSelectMultiple(),
            "producto": forms.CheckboxSelectMultiple(),
            "activa": forms.CheckboxInput()
        }
        localized_fields = ["inicio_promo", "fin_promo"]

    def clean(self):
        cleaned_data = super().clean()
        usuarios = cleaned_data.get('usuarios')
        descuento = cleaned_data.get('descuento')
        inicio_promo = cleaned_data.get('inicio_promo')
        fin_promo = cleaned_data.get('fin_promo')
        producto = cleaned_data.get('producto')

        if descuento is not None:
            if descuento < 0 or descuento > 10:
                self.add_error('descuento', 'El descuento debe estar entre 0 y 10')

        if inicio_promo and fin_promo:
            if inicio_promo >= fin_promo:
                self.add_error('inicio_promo', 'La promo de inicio debe ser anterior a la promo de fin')
                self.add_error('fin_promo', 'La promo de fin debe ser posterior a la promo de inicio')

        if producto and not producto.puede_tener_promociones:
            self.add_error('producto', 'Este producto no permite promociones')

        if usuarios:
            menores = usuarios.filter(edad__lt=18)
            if menores.exists():
                self.add_error('usuarios', 'Todos los usuarios deben ser mayores de edad')

        return cleaned_data



class PromocionSearchForm(forms.Form):
    search_text = forms.CharField(
        required=False,
        label='Buscar en nombre/descripción',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    fecha_fin_menor = forms.DateField(
        required=False,
        label='Fecha fin menor que',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    fecha_fin_mayor = forms.DateField(
        required=False,
        label='Fecha fin mayor que',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    descuento_mayor = forms.IntegerField(
        required=False,
        label='Descuento mayor que',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    usuarios = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Usuario.objects.all(),
        label='Usuarios',
        widget=forms.CheckboxSelectMultiple
    )
    
    activa = forms.BooleanField(
        required=False,
        label='Solo promociones activas',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
     



   