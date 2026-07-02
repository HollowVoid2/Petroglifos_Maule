from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Simbolo, ArchivoMultimedia


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultiFileField(forms.FileField):
    def to_python(self, data):
        if not data:
            return []
        if isinstance(data, (list, tuple)):
            return list(data)
        return [data]

    def validate(self, data):
        if self.required and not data:
            raise forms.ValidationError('Debes seleccionar al menos un archivo.')
        for item in data:
            super().validate(item)


class SimboloForm(forms.ModelForm):
    class Meta:
        model = Simbolo
        fields = ['panel', 'codigo', 'descripcion', 'iconografia', 'estado_conservacion']
        labels = {
            'panel': 'Panel al que pertenece',
            'codigo': 'Código de Identificación (Ej: SIM-02)',
            'descripcion': 'Descripción Detallada',
            'iconografia': 'Tipo o Motivo (Iconografia)',
            'estado_conservacion': 'Estado de Conservación',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }


class ArchivoMultimediaForm(forms.ModelForm):
    class Meta:
        model = ArchivoMultimedia
        fields = ['archivo', 'es_principal']
        labels = {
            'archivo': 'Archivo de Imagen Principal',
            'es_principal': '¿Es la imagen principal?',
        }


class ArchivosMultipleForm(forms.Form):
    archivos = MultiFileField(
        required=False,
        label='Galeria de imagenes (puedes seleccionar varias) ',
        widget=MultiFileInput(attrs={'multiple': True})
    )


class InvestigadorCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo',
            'password1': 'Contrasena',
            'password2': 'Confirmar contrasena',
        }
