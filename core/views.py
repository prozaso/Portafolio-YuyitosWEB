import base64
from django.shortcuts import render, redirect
from django.db import connection, models
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import cx_Oracle
from .forms import CustomUserForm, ProductoForm, FamiliaForm, TipoForm, PedidoForm
#from django.contrib.auth.decorators import login_required, permission_required
from .models import FamiliaProducto, Producto

#imports necesarios para enviar correo
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


# Create your views here.
def home(request):

    data = {
        'productos':lista_productos(),

    }

    return render(request, 'core/home.html', data)


def productos(request):

    data = {
        'productos':lista_productos_detallado(),

    }

    if 'modificar' in request.POST:
        if request.method == 'POST':

            idprod = request.POST.get('id')
            print(idprod)

    return render(request, 'core/lista_productos.html', data)


def nosotros(request):

    data = {
        'nosotros':lista_nosotros(),
        'seleccionado':nosotros_seleccionado(),

    }

    if 'seleccionar' in request.POST:
        if request.method == 'POST':

            idseleccion = request.POST.get('cbonosotros')
            salida = seleccionar_nosotros(idseleccion)

            if salida == 1:
                data['mensaje'] = 'Cambio realizado exitosamente'
            else:
                data['mensaje'] = 'El cambio no se pudo realizar'

    if 'nuevonosotros' in request.POST:
        if request.method == 'POST':

            titulo_pagina = request.POST.get('titulo_pagina')
            titulo_mision = request.POST.get('titulo_mision')
            descripcion_mision = request.POST.get('descripcion_mision')
            titulo_vision = request.POST.get('titulo_vision')
            descripcion_vision = request.POST.get('descripcion_vision')

            salida = agregar_nosotros(titulo_pagina, titulo_mision, titulo_vision,
                                      descripcion_mision, descripcion_vision)

            if salida == 1:
                data['mensaje2'] = 'Agregado exitosamente'
            else:
                data['mensaje2'] = 'No se pudo agregar'

    return render(request, 'core/nosotros.html', data)


#listamos todos los nosotros en la BD
def lista_nosotros():

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_NOSOTROS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista

#guardamos el nosotros seleccionado
def seleccionar_nosotros(nosotrosid):

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_SELECCIONAR_NOSOTROS', [nosotrosid, salida])

    return salida.getvalue()

#traemos el nosotros seleccionado
def nosotros_seleccionado():

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_NOSOTROS_SELECCIONADO", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def agregar_nosotros(titulo_pagina, titulo_mision, titulo_vision, descripcion_mision,
                     descripcion_vision):

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_NOSOTROS', [titulo_pagina, titulo_mision, titulo_vision,
                                            descripcion_mision, descripcion_vision, salida])

    return salida.getvalue()


#metodo para enviar correo
def send_email(mail, nombre, mensaje):

    context = {'mail':mail,
               'nombre':nombre,
               'mensaje':mensaje}

    template = get_template('core/correo.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Nuevo mensaje desde la web!',
        'CodigoFacilito',
        mail,
        [settings.EMAIL_HOST_USER]
    )

    email.attach_alternative(content, 'text/html')
    email.send()

#enviar correo
def contacto(request):

    data = {}

    if request.method == 'POST':

        mail = request.POST.get('correo')
        nombre = request.POST.get('nombre')
        mensaje = request.POST.get('mensaje')

        send_email(mail, nombre, mensaje)

        data['mensaje'] = 'Mensaje enviado con exito'


    return render(request, 'core/contacto.html', data)


def base(request):

    data = {
        'productos':lista_productos()
    }

    return render(request, 'core/base.html', data)


def nuevo_producto(request):

    data = {
        'productos':lista_productos(),
        'familias':lista_familias(),
        'medidas':lista_medidas(),
        'tipos':lista_tipos(),
        'proveedores':lista_proveedores(),

    }

    if 'guardar' in request.POST:
        if request.method == 'POST':
            nombre_producto = request.POST.get('nombre')
            tipo_prod_id_tip_prod = request.POST.get('cbotipo')
            id_familia = request.POST.get('cbofamilia')
            precio_compra = request.POST.get('precio_c')
            precio_venta = request.POST.get('precio_v')
            stock = request.POST.get('stock')
            stock_c = request.POST.get('stock_c')
            kilos_litros_id_kg_lt = request.POST.get('cboumedida')
            descripcion = request.POST.get('desc')
            fecha_vencimiento = request.POST.get('fecha_v')
            proveedor_id_prov = request.POST.get('cboproveedor')
            imagen = request.FILES['imagen'].read()
            salida = agregar_producto(nombre_producto, precio_compra, precio_venta,
                                      stock, stock_c, kilos_litros_id_kg_lt, descripcion,
                                      tipo_prod_id_tip_prod, id_familia, fecha_vencimiento, 
                                      proveedor_id_prov, imagen)
            if salida == 1:
                data['mensaje'] = 'agregado correctamente'
            else:
                data['mensaje'] = 'no se ha podido guardar'


    return render(request, 'core/nuevo_producto.html', data)


def galeria_productos(request):

    data = {
        'productos':lista_productos(),
        'tipos':lista_tipos(),

    }
    return render(request, 'core/galeria_productos.html', data)


def lista_productos():

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PRODUCTOS", [out_cur])

    lista = []
    for fila in out_cur:
        data = {
            'data':fila,
            'imagen':str(base64.b64encode(fila[12].read()), 'utf-8')
        }
        lista.append(data)

    return lista


def lista_productos_detallado():

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PRODUCTOS_DETALLADO", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def lista_productos_pedido():

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PRODUCTOS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def lista_proveedores():

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PROVEEDORES", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def lista_familias():

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_FAMILIAS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def lista_tipos():

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_TIPOS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def lista_tipos_por_familia(familiaid):

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_TIPO_POR_FAMILIA", [familiaid, out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def tipos_por_familia(request):

    familia = request.GET.get('familiaid')
    data = {
        'tipos':lista_tipos_por_familia(familia)
    }

    return render(request, 'core/options_tipos_productos.html', data)


def lista_productos_por_tipo(tipoid):

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_PRODUCTOS_POR_TIPO", [tipoid, out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def productos_por_tipo(request):

    tipo = request.GET.get('tipoid')
    data = {
        'productos':lista_productos_por_tipo(tipo)
    }

    return render(request, 'core/options_productos_por_tipos.html', data)


def lista_medidas():

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_MEDIDAS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def agregar_producto(nombre_producto, precio_compra, precio_venta,
                     stock, stock_c, kilos_litros_id_kg_lt, descripcion,
                     tipo_prod_id_tip_prod, id_familia, fecha_vencimiento,
                     proveedor_id_prov, imagen):

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_PRODUCTO', [nombre_producto, precio_compra, precio_venta,
                                            stock, stock_c, kilos_litros_id_kg_lt, descripcion,
                                            tipo_prod_id_tip_prod, id_familia, fecha_vencimiento,
                                            proveedor_id_prov, imagen, salida])

    return salida.getvalue()


def modificar_producto(id_prod, nombre_producto, precio_compra, precio_venta,
                       stock, stock_c, kilos_litros_id_kg_lt, descripcion, 
                       fecha_vencimiento, tipo_prod_id_tip_prod, proveedor_id_prov, imagen):

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_PRODUCTO', [id_prod, nombre_producto, precio_compra, precio_venta,
                                             stock, stock_c, kilos_litros_id_kg_lt, descripcion,
                                             fecha_vencimiento, tipo_prod_id_tip_prod, proveedor_id_prov,
                                             imagen, salida])

    return salida.getvalue()


def modificar_producto_sin_img(id_prod, nombre_producto, precio_compra, precio_venta,
                       stock, stock_c, kilos_litros_id_kg_lt, descripcion, 
                       fecha_vencimiento, tipo_prod_id_tip_prod, proveedor_id_prov):

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_PRODUCTO_SIN_IMG', [id_prod, nombre_producto, precio_compra, precio_venta,
                                             stock, stock_c, kilos_litros_id_kg_lt, descripcion,
                                             fecha_vencimiento, tipo_prod_id_tip_prod, proveedor_id_prov,
                                             salida])

    return salida.getvalue()


def eliminar_producto(producto):

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_ELIMINAR_PRODUCTO', [producto, salida])

    return salida.getvalue()


def modificar_producto_template(request):

    data = {
        'productos':lista_productos(),
        'familias':lista_familias(),
        'medidas':lista_medidas(),
        'tipos':lista_tipos(),
        'proveedores':lista_proveedores(),

    }

    if 'prodid' in request.POST:
        if request.method == 'POST':

            prodid = request.POST.get('cboprod')
            producto = producto_por_id_detallado(prodid)

            data['prod'] = producto


    if 'guardar' in request.POST:
        if request.method == 'POST':
            id_prod = request.POST.get('cboprod')
            nombre_producto = request.POST.get('nombre')
            tipo_prod_id_tip_prod = request.POST.get('cbotipo')
            precio_compra = request.POST.get('precio_c')
            precio_venta = request.POST.get('precio_v')
            stock = request.POST.get('stock')
            stock_c = request.POST.get('stock_c')
            kilos_litros_id_kg_lt = request.POST.get('cboumedida')
            descripcion = request.POST.get('desc')
            fecha_vencimiento = request.POST.get('fecha_v')
            proveedor_id_prov = request.POST.get('cboproveedor')
            imagen = request.FILES.get('imagen', False)

            imagen = request.FILES['imagen'] if 'imagen' in request.FILES else False

            if imagen == False:
                salida = modificar_producto_sin_img(id_prod, nombre_producto, precio_compra, precio_venta,
                                        stock, stock_c, kilos_litros_id_kg_lt, descripcion, 
                                        fecha_vencimiento, tipo_prod_id_tip_prod, proveedor_id_prov)
            else:
                salida = modificar_producto(id_prod, nombre_producto, precio_compra, precio_venta,
                                        stock, stock_c, kilos_litros_id_kg_lt, descripcion, 
                                        fecha_vencimiento, tipo_prod_id_tip_prod, proveedor_id_prov,
                                        imagen)

            if salida == 1:
                data['mensaje'] = 'Cambios guardados correctamente'
            else:
                data['mensaje'] = 'No se ha podido guardar los cambios'

    if 'eliminar' in request.POST:
        if request.method == 'POST':

            prodid = request.POST.get('cboprod')
            salida = eliminar_producto(prodid)
            print(salida)

            if salida == 1:
                data['eliminado'] = 'Producto eliminado satisfactoriamente'
            else:
                data['eliminado'] = 'Producto no se pudo eliminar'
                

    return render(request, 'core/modificar_producto.html', data)


def registro_usuario(request):

    data = {
        
    }


    return render(request, 'registration/registrar.html', data)


def productos_en_pedido(request):

    producto = request.GET.get('prodid')
    productos = []
    productos.append(producto_por_id(producto))

    data = {
        'lista_productos_pedido':producto_por_id(producto),
    }

    return render(request, 'core/lista_productos_pedido.html', data)


def producto_por_id(prodid):

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc('SP_PRODUCTO_POR_ID', [prodid, out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def producto_por_id_detallado(prodid):

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc('SP_PRODUCTO_POR_ID_DETALLADO', [prodid, out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def lista_pedidos():

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PEDIDOS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def producto_por_nombre(pnombre):

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc('SP_PRODUCTO_POR_NOMBRE', [pnombre, out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


@csrf_exempt
def nuevo_pedido(request):

    data = {
        'productos_cbo':lista_productos_pedido(),
        'productos':lista_productos(),
        'proveedores':lista_proveedores(),
        'tipos':lista_tipos(),
        'familias':lista_familias(),
        'pedidos':lista_pedidos(),
    }

    if 'crearpedido' in request.POST:
        if request.method == 'POST':

            #si el usuario esta logeado lo obtenemos con request.user
            if request.user.is_authenticated:
                #guardamos el usuario en current_user
                current_user = request.user

            fecha_pedido = request.POST.get('fecha_pedido')

            #desde el usuario guardado en current_user obtenemos su id y la utilizamos
            salida = ingresar_pedido(fecha_pedido, current_user.id)

            if salida == 1:
                data['mensaje'] = 'Creado correctamente'
            else:
                data['mensaje'] = 'No se ha podido crear'

    if 'agregarproducto' in request.POST:
        if request.method == 'POST':

            producto = request.POST.get('cboprod')
            cantidad = request.POST.get('cantidad')
            pedido = request.POST.get('cbopedido')

            salida = ingresar_detalle_pedido(producto, cantidad, pedido)
            if salida == 1:
                data['mensaje2'] = 'Agregado correctamente'
            else:
                data['mensaje2'] = 'No se ha podido agregar'

            salida = pedido_por_id(pedido)
            salida2 = valor_pedido_por_id(pedido)

            data['pedido'] = salida
            data['total'] = salida2

    if 'verpedido' in request.POST:
        if request.method == 'POST':

            idpedido = request.POST.get('cboverpedido')

            salida = pedido_por_id(idpedido)
            salida2 = valor_pedido_por_id(idpedido)

            data['pedido'] = salida
            data['total'] = salida2

    return render(request, 'core/nuevo_pedido.html', data)


def ingresar_pedido(fecha_pedido, usuario):

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_CREAR_PEDIDO', [fecha_pedido, usuario, salida])

    return salida.getvalue()


def ingresar_detalle_pedido(producto, cantidad, pedido):

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_DETALLE_PEDIDO', [producto, cantidad, pedido, salida])

    return salida.getvalue()


def pedido_por_id(pedidoid):

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc('SP_PEDIDO_POR_ID', [pedidoid, out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def valor_pedido_por_id(pedidoid):

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc('SP_VALOR_PEDIDO', [pedidoid, out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def ventas(request):

    data = {
        'productos_cbo':lista_productos_pedido(),
        'productos':lista_productos(),
        'tipos':lista_tipos(),
        'familias':lista_familias(),
        'ventas':lista_ventas(),
    }

    if 'crearventa' in request.POST:
        if request.method == 'POST':

            #si el usuario esta logeado lo obtenemos con request.user
            if request.user.is_authenticated:
                #guardamos el usuario en current_user
                current_user = request.user

            fecha_venta = request.POST.get('fecha_venta')
            venta = request.POST.get('cboventa')

            #desde el usuario guardado en current_user obtenemos su id y la utilizamos
            salida = ingresar_venta(fecha_venta, current_user.id)

            if salida == 1:
                data['mensaje'] = 'Creada correctamente'

                salida1 = venta_por_id(venta)
                salida2 = valor_venta_por_id(venta)

                data['venta'] = salida1
                data['total'] = salida2
            else:
                data['mensaje'] = 'No se ha podido crear'

    if 'agregarproducto' in request.POST:
        if request.method == 'POST':

            producto = request.POST.get('cboprod')
            cantidad = request.POST.get('cantidad')
            venta = request.POST.get('cboventa')

            if buscar_boleta_venta(venta):
                data['ventaConBoleta'] = 'No se pueden agregar productos a una venta con boleta'
            else:
                salida = ingresar_detalle_venta(producto, cantidad, venta)

                if salida == 1:
                    data['mensaje2'] = 'Agregado correctamente'
                else:
                    data['mensaje2'] = 'No se ha podido agregar'            

            salida1 = venta_por_id(venta)
            salida2 = valor_venta_por_id(venta)

            data['venta'] = salida1
            data['total'] = salida2

    if 'verventa' in request.POST:
        if request.method == 'POST':

            idventa = request.POST.get('cboverventa')

            salida1 = venta_por_id(idventa)
            salida2 = valor_venta_por_id(idventa)

            data['venta'] = salida1
            data['total'] = salida2

    if 'crearboleta' in request.POST:
        if request.method == 'POST':

            #si el usuario esta logeado lo obtenemos con request.user
            if request.user.is_authenticated:
                #guardamos el usuario en current_user
                current_user = request.user

            venta = request.POST.get('cboverventa')
            fiada = request.POST.get('switch')

            existe = buscar_boleta_venta(venta)
            print(existe)

            if existe:
                data['mensaje3'] = 'La venta seleccionada ya posee boleta'
            else:
                if fiada == 'on':
                    salida = crear_boleta_fiada(venta, current_user.id)
                else:
                    salida = crear_boleta(venta, current_user.id)

    return render(request, 'core/ventas.html', data)


def ingresar_venta(fecha_venta, usuario):

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_CREAR_VENTA', [fecha_venta, usuario, salida])

    return salida.getvalue()


def ingresar_detalle_venta(producto, cantidad, venta):

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_DETALLE_VENTA', [producto, cantidad, venta, salida])

    return salida.getvalue()


def venta_por_id(ventaid):

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc('SP_VENTA_POR_ID', [ventaid, out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def valor_venta_por_id(ventaid):

    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc('SP_VALOR_VENTA', [ventaid, out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def lista_ventas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_VENTAS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


def crear_boleta(venta, usuario):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_CREAR_BOLETA', [venta, usuario, salida])

    return salida.getvalue()


def crear_boleta_fiada(venta, usuario):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_CREAR_BOLETA_FIADA', [venta, usuario, salida])

    return salida.getvalue()


def buscar_boleta_venta(bolid):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc('SP_BUSCAR_BOLETA_VENTA', [bolid, out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista
