# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Abono(models.Model):
    id_abono = models.FloatField(primary_key=True)
    monto_abonado = models.BigIntegerField()
    boleta_id_bol = models.ForeignKey('Boleta', models.DO_NOTHING, db_column='boleta_id_bol')
    fecha_abono = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'abono'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Boleta(models.Model):
    id_bol = models.FloatField(primary_key=True)
    fiado = models.FloatField()
    estado_pago = models.FloatField()
    total_boleta = models.BigIntegerField()
    venta_id_vent = models.ForeignKey('Venta', models.DO_NOTHING, db_column='venta_id_vent')
    usuario_id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario_id_usuario', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boleta'


class Comuna(models.Model):
    id_comu = models.FloatField(primary_key=True)
    region_id_reg = models.ForeignKey('Region', models.DO_NOTHING, db_column='region_id_reg', blank=True, null=True)
    nombre_comuna = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'comuna'


class DetallePedido(models.Model):
    id_det_ped = models.FloatField(primary_key=True)
    producto_id_prod = models.ForeignKey('Producto', models.DO_NOTHING, db_column='producto_id_prod', blank=True, null=True)
    cantidad_prod_p = models.BigIntegerField()
    pedido_id_pedido = models.ForeignKey('Pedido', models.DO_NOTHING, db_column='pedido_id_pedido', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalle_pedido'

    def ___str___(self):
        return self.id_det_ped


class DetalleVenta(models.Model):
    id_det_ven = models.FloatField(primary_key=True)
    venta_id_vent = models.ForeignKey('Venta', models.DO_NOTHING, db_column='venta_id_vent', blank=True, null=True)
    cantidad_prod_v = models.BigIntegerField()
    producto_id_prod = models.ForeignKey('Producto', models.DO_NOTHING, db_column='producto_id_prod', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalle_venta'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Errores(models.Model):
    id_error = models.FloatField(primary_key=True)
    mensaje_error = models.CharField(max_length=500)
    codigo_error = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'errores'


class Estadisticas(models.Model):
    id_est = models.FloatField(primary_key=True)
    tipo_estad_id_tipo = models.BigIntegerField(blank=True, null=True)
    nombre_estadistica = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'estadisticas'


class EstadoPedido(models.Model):
    id_estado = models.FloatField(primary_key=True)
    descripcion_estado = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'estado_pedido'


class FamiliaProducto(models.Model):
    id_familia = models.FloatField(primary_key=True)
    nombre_familia = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'familia_producto'


class KilosLitros(models.Model):
    id_kg_lt = models.FloatField(primary_key=True)
    descripcion_kg_lt = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'kilos_litros'


class Nosotros(models.Model):
    id_nosotros = models.FloatField(primary_key=True)
    titulo_pagina = models.CharField(max_length=50)
    titulo_mision = models.CharField(max_length=50)
    titulo_vision = models.CharField(max_length=50)
    descripcion_mision = models.CharField(max_length=1000)
    descripcion_vision = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'nosotros'


class Pedido(models.Model):
    id_pedido = models.FloatField(primary_key=True)
    fecha_pedido = models.CharField(max_length=10)
    usuario_id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario_id_usuario', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pedido'

    def ___str___(self):
        return self.fecha_pedido


class Producto(models.Model):
    id_prod = models.FloatField(primary_key=True)
    nombre_producto = models.CharField(max_length=200)
    precio_compra = models.BigIntegerField()
    precio_venta = models.BigIntegerField()
    stock = models.BigIntegerField()
    stock_critico = models.FloatField()
    codigo_barra = models.BigIntegerField()
    kilos_litros_id_kg_lt = models.ForeignKey(KilosLitros, models.DO_NOTHING, db_column='kilos_litros_id_kg_lt')
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    fecha_vencimiento = models.CharField(max_length=10, blank=True, null=True)
    tipo_prod_id_tip_prod = models.ForeignKey('TipoProd', models.DO_NOTHING, db_column='tipo_prod_id_tip_prod')
    proveedor_id_prov = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='proveedor_id_prov', blank=True, null=True)
    imagen = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'producto'

    def ___str___(self):
        return self.nombre_producto


class Proveedor(models.Model):
    id_prov = models.FloatField(primary_key=True)
    nombre_proveedor = models.CharField(max_length=200)
    comuna_id_comu = models.ForeignKey(Comuna, models.DO_NOTHING, db_column='comuna_id_comu')
    direccion_proveedor = models.CharField(max_length=200)
    telefono_proveedor = models.CharField(max_length=12)
    correo_proveedor = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'proveedor'


class RecepPedido(models.Model):
    id_recep_p = models.FloatField(primary_key=True)
    proveedor_id_prov = models.ForeignKey(Proveedor, models.DO_NOTHING, db_column='proveedor_id_prov')
    fecha_recp = models.CharField(max_length=10)
    estado_pedido_id_estado = models.ForeignKey(EstadoPedido, models.DO_NOTHING, db_column='estado_pedido_id_estado')
    pedido_id_pedido = models.ForeignKey(Pedido, models.DO_NOTHING, db_column='pedido_id_pedido')

    class Meta:
        managed = False
        db_table = 'recep_pedido'


class Region(models.Model):
    id_reg = models.FloatField(primary_key=True)
    nombre_region = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'region'


class TipoProd(models.Model):
    id_tip_prod = models.FloatField(primary_key=True)
    nombre_tipo = models.CharField(max_length=100)
    familia_producto_id_familia = models.ForeignKey(FamiliaProducto, models.DO_NOTHING, db_column='familia_producto_id_familia', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_prod'


class TipoUser(models.Model):
    id_tipo_u = models.FloatField(primary_key=True)
    nom_tipo_u = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'tipo_user'


class Usuario(models.Model):
    id_usuario = models.FloatField(primary_key=True)
    comuna_id_comu = models.ForeignKey(Comuna, models.DO_NOTHING, db_column='comuna_id_comu', blank=True, null=True)
    nombre = models.CharField(max_length=30)
    apellido_m = models.CharField(max_length=30)
    apellido_p = models.CharField(max_length=30)
    fecha_nac = models.CharField(max_length=10, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    rut = models.CharField(max_length=12)
    tipo_user_id_tipo_u = models.ForeignKey(TipoUser, models.DO_NOTHING, db_column='tipo_user_id_tipo_u', blank=True, null=True)
    password = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'usuario'


class Venta(models.Model):
    id_vent = models.FloatField(primary_key=True)
    fecha_venta = models.CharField(max_length=10)
    usuario_id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='usuario_id_usuario', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'venta'
