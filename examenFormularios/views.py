from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html') 

 
def lista_promociones(request):
    promociones = Promocion.objects.select_related("producto").prefetch_related("usuarios")
    return render(request, 'promocion/lista_promociones.html', {"promociones": promociones})


def busqueda_avanzada_promociones(request):
    form = PromocionSearchForm(request.GET or None)
    promociones = Promocion.objects.all()

    if form.is_valid():
    	
        if form.cleaned_data.get('search_text'):
            search_query = form.cleaned_data['search_text']
            promociones = promociones.filter(
            	Q(nombre__icontains=search_query) |
            	Q(descripcion__icontains=search_query)
        	)
     
        if form.cleaned_data.get('fecha_fin_menor'):
            promociones = promociones.filter(
                fin_promo__lte=form.cleaned_data['fecha_fin_menor']
        	)
   	 
    	
        if form.cleaned_data.get('fecha_fin_mayor'):
            promociones = promociones.filter(
                fin_promo__gte=form.cleaned_data['fecha_fin_mayor']
            )
   	 
    	
        if form.cleaned_data.get('descuento_mayor') is not None:
            promociones = promociones.filter(
                descuento__gt=form.cleaned_data['descuento_mayor']
            )
   	 
    	
        if form.cleaned_data.get('usuarios'):
            promociones = promociones.filter(
                usuarios__in=form.cleaned_data['usuarios']
            ).distinct()
   	 
    	
        if form.cleaned_data.get('activa'):
            promociones = promociones.filter(activa=True)
    
    return render(request, 'promocion/busqueda_promociones.html', {'form': form,
    	'promociones': promociones})

def crear_promocion(request):

    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = PromocionModelForm(datosFormulario)

    if request.method == "POST":
        promo_creada = crear_promocion_modelo(formulario)
        if(promo_creada):
            messages.success(request, 'Se ha creado el libro '+formulario.cleaned_data.get('nombre')+" correctamente")
            return redirect("lista_promociones")
    
    return render(request, 'promocion/crear_promocion.html',{"formulario":formulario})


def promocion_editar(request,promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    
    formulario = PromocionModelForm(datosFormulario,instance = promocion)
    
    if (request.method == "POST"):
       
        if formulario.is_valid():
            try:  
                formulario.save()
                messages.success(request, 'Se ha editado la promocion'+formulario.cleaned_data.get('nombre')+" correctamente")
                return redirect('promocion_lista')  
            except Exception as error:
                print(error)
    return render(request, 'promocion/actualizar_promocion.html',{"formulario":formulario,"promocion":promocion})


def promocion_eliminar(request,promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)
    try:
        promocion.delete()
        messages.success(request, "Se ha elimnado el promocion "+promocion.nombre+" correctamente")
    except Exception as error:
        print(error)
    return redirect('lista_promociones')



def crear_promocion_modelo(formulario):
    
    promocion = False
    if formulario.is_valid():
        try:
            
            formulario.save()
            promocion = True
        except Exception as error:
            print(error)
    return promocion




