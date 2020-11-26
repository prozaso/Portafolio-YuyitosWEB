from django.conf.urls import url
from django.urls import path
from core import views
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('galeria_productos/', galeria_productos, name="galeria_productos"),
    path('nuevo_producto/', nuevo_producto, name="nuevo_producto"),
    path('nuevo_pedido/', nuevo_pedido, name="nuevo_pedido"),
    path('tipos/', tipos_por_familia, name="tipos_por_familia"),
    path('productos/', productos_por_tipo, name="productos_por_tipo"),
    path('productos_pedido/', productos_en_pedido, name="productos_pedido"),
    path('contacto', contacto, name="contacto"),
    path('nosotros', nosotros, name="nosotros"),
    path('lista_productos', productos, name="productos"),
    path('ventas', ventas, name="ventas"),
    path('modificar_producto', modificar_producto_template, name="modificar_producto"),
    path('registrar', registro_usuario, name="registrar"),

]
