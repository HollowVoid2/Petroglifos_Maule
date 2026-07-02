from django.db import models
from django.contrib.auth.models import User


class Sitio(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    coordenadas_gps = models.CharField(max_length=100, help_text="Coordenadas GPS obligatorias")
    comuna = models.CharField(max_length=100)
    # Soft delete fields
    esta_activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    justificacion_desactivacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Bloque(models.Model):
    sitio = models.ForeignKey(Sitio, on_delete=models.CASCADE, related_name='bloques')
    codigo = models.CharField(max_length=50, help_text="Ej: BL-01")
    # Soft delete fields
    esta_activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sitio.nombre} - {self.codigo}"


class Panel(models.Model):
    bloque = models.ForeignKey(Bloque, on_delete=models.CASCADE, related_name='paneles')
    codigo = models.CharField(max_length=50, help_text="Ej: PA-01")
    # Soft delete fields
    esta_activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bloque} - {self.codigo}"


class Simbolo(models.Model):
    ESTADO_CHOICES = [
        ('BUENO', 'Bueno'),
        ('ACEPTABLE', 'Aceptable'),
        ('EN_RIESGO', 'En riesgo'),
        ('MALO', 'Malo'),
        ('SIN_DATOS', 'Sin evaluar'),
    ]

    panel = models.ForeignKey(Panel, on_delete=models.CASCADE, related_name='simbolos')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='simbolos_creados')
    codigo = models.CharField(max_length=50, help_text="Ej: SIM-01")
    descripcion = models.TextField(blank=True, null=True)
    iconografia = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="Tipo o motivo representado (iconografia)"
    )
    estado_conservacion = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        blank=True,
        null=True
    )
    # Soft delete fields
    esta_activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.panel} - {self.codigo}"


class ArchivoMultimedia(models.Model):
    TIPO_CHOICES = [
        ('FOTO', 'Fotografía'),
        ('CALCO', 'Calco Digital'),
    ]
    simbolo = models.ForeignKey(Simbolo, on_delete=models.CASCADE, related_name='multimedia')
    tipo_archivo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    # Usamos FileField para que Django gestione la subida de archivos
    archivo = models.FileField(upload_to='multimedia/', help_text="Soporta JPG, PNG, PDF. Max 50MB")
    es_principal = models.BooleanField(default=False, help_text="Marcar si es la imagen principal del símbolo")
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.simbolo} - {self.get_tipo_archivo_display()}"
