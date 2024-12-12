from django.urls import path, re_path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    
    path('promocion/create/',views.crear_promocion,name='crear_promocion'), 
    
    path('promocion/listar',views.lista_promociones,name='lista_promociones'),
    
    path('promocion/editar/<int:promocion_id>',views.promocion_editar,name='promocion_editar'),
    
    path('promocion/busqueda_avanzada/', views.busqueda_avanzada_promociones, name='busqueda_promociones'),


    path('promocion/eliminar/<int:promocion_id>',views.promocion_eliminar,name='promocion_eliminar'),
]