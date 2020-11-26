from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Producto, FamiliaProducto, TipoProd, Pedido


class CustomUserForm(UserCreationForm):

    username = forms.CharField(required=True, label='Nombre de usuario')
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    first_name = forms.CharField(min_length=3, max_length=80, required=True, label='Nombre')
    last_name = forms.CharField(min_length=3, max_length=80, required=True, label='Apellido')
    email = forms.EmailField(required=True, label='Correo electrónico')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

    def clean_email(self):

        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Correo ya existe")
        return email

class ProductoForm(ModelForm):

    class Meta:
        model = Producto
        fields = ['nombre_producto',
                  'precio_compra', 'precio_venta', 'stock',
                  'stock_critico', 'codigo_barra', 'kilos_litros_id_kg_lt', 'descripcion',
                  'tipo_prod_id_tip_prod', 'fecha_vencimiento']

class FamiliaForm(ModelForm):

    class Meta:
        model = FamiliaProducto
        fields = ['id_familia', 'nombre_familia']

class TipoForm(ModelForm):

    class Meta:
        model = TipoProd
        fields = ['id_tip_prod', 'familia_producto_id_familia', 'nombre_tipo']

class PedidoForm(ModelForm):

    class Meta:
        model = Pedido
        fields = ['id_pedido', 'fecha_pedido', 'usuario_id_usuario']
