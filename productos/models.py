from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    direccion = models.TextField()  
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True,
    )

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    categorias = models.ManyToManyField(Categoria)  

    def __str__(self):
        return self.nombre

class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"

class Carrito(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)

    def total_pagar(self):
        return sum(producto.precio for producto in self.productos.all())

    def cantidad_productos(self):
        return self.productos.count()

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class Envio(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)
    direccion = models.TextField()
    estado = models.CharField(max_length=50, choices=[
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado')
    ], default='pendiente')

    def __str__(self):
        return f"Envío para {self.usuario.username} - Estado: {self.estado}"
