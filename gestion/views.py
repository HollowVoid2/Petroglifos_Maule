from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseForbidden
from django.conf import settings
from .models import Simbolo, ArchivoMultimedia
from .forms import SimboloForm, ArchivosMultipleForm, InvestigadorCreationForm


def _adjuntar_imagen_principal(simbolos):
    for simbolo in simbolos:
        imagen_principal = simbolo.multimedia.filter(es_principal=True).first()
        if imagen_principal and imagen_principal.archivo:
            simbolo.imagen_url = imagen_principal.archivo.url
        else:
            simbolo.imagen_url = None
    return simbolos


@login_required
def catalogo_mis_investigaciones(request):
    simbolos = Simbolo.objects.filter(
        esta_activo=True,
        autor=request.user
    ).order_by('-fecha_modificacion')
    simbolos = _adjuntar_imagen_principal(simbolos)
    context = {
        'simbolos': simbolos,
        'vista': 'mis',
        'titulo': 'Mis Investigaciones'
    }
    return render(request, 'gestion/catalogo.html', context)


@login_required
def catalogo_todas_investigaciones(request):
    simbolos = Simbolo.objects.filter(esta_activo=True).order_by('-fecha_modificacion')
    simbolos = _adjuntar_imagen_principal(simbolos)
    context = {
        'simbolos': simbolos,
        'vista': 'todas',
        'titulo': 'Todas las Investigaciones'
    }
    return render(request, 'gestion/catalogo.html', context)


@login_required
def simbolo_detalle(request, simbolo_id):
    """Muestra la información detallada de un único símbolo."""
    simbolo = get_object_or_404(Simbolo, pk=simbolo_id, esta_activo=True)
    archivos_multimedia = simbolo.multimedia.all()
    vista = request.GET.get('vista', 'mis')
    volver_url = 'gestion:catalogo_todas' if vista == 'todas' else 'gestion:mis_investigaciones'

    can_edit = request.user.is_superuser or simbolo.autor == request.user

    context = {
        'simbolo': simbolo,
        'archivos_multimedia': archivos_multimedia,
        'volver_url': volver_url,
        'vista': vista,
        'can_edit': can_edit
    }
    return render(request, 'gestion/simbolo_detalle.html', context)


@login_required
def crear_simbolo(request):
    """Muestra un formulario para crear un nuevo símbolo y su galeria."""
    if request.method == 'POST':
        simbolo_form = SimboloForm(request.POST)
        archivos_form = ArchivosMultipleForm(request.POST, request.FILES)

        if simbolo_form.is_valid() and archivos_form.is_valid():
            nuevo_simbolo = simbolo_form.save(commit=False)
            nuevo_simbolo.autor = request.user
            nuevo_simbolo.save()

            archivos = archivos_form.cleaned_data.get('archivos', [])
            principal_asignado = False
            for archivo in archivos:
                ArchivoMultimedia.objects.create(
                    simbolo=nuevo_simbolo,
                    tipo_archivo='FOTO',
                    archivo=archivo,
                    es_principal=not principal_asignado
                )
                principal_asignado = True

            return redirect('gestion:mis_investigaciones')
    else:
        simbolo_form = SimboloForm()
        archivos_form = ArchivosMultipleForm()

    context = {
        'simbolo_form': simbolo_form,
        'archivos_form': archivos_form,
        'titulo': 'Añadir Nueva Investigación'
    }
    return render(request, 'gestion/simbolo_form.html', context)


@login_required
def editar_simbolo(request, simbolo_id):
    simbolo = get_object_or_404(Simbolo, pk=simbolo_id, esta_activo=True)
    if not (request.user.is_superuser or simbolo.autor == request.user):
        return HttpResponseForbidden('No tienes permisos para editar este simbolo.')

    if request.method == 'POST':
        simbolo_form = SimboloForm(request.POST, instance=simbolo)
        archivos_form = ArchivosMultipleForm(request.POST, request.FILES)

        if simbolo_form.is_valid() and archivos_form.is_valid():
            simbolo_form.save()

            eliminar_ids = request.POST.getlist('eliminar_ids')
            if eliminar_ids:
                for media in simbolo.multimedia.filter(id__in=eliminar_ids):
                    media.delete()

            principal_id = request.POST.get('principal_id')
            if principal_id:
                simbolo.multimedia.update(es_principal=False)
                simbolo.multimedia.filter(id=principal_id).update(es_principal=True)

            archivos = archivos_form.cleaned_data.get('archivos', [])
            principal_existente = simbolo.multimedia.filter(es_principal=True).exists()
            for archivo in archivos:
                ArchivoMultimedia.objects.create(
                    simbolo=simbolo,
                    tipo_archivo='FOTO',
                    archivo=archivo,
                    es_principal=not principal_existente
                )
                principal_existente = True

            return redirect('gestion:simbolo_detalle', simbolo_id=simbolo.id)
    else:
        simbolo_form = SimboloForm(instance=simbolo)
        archivos_form = ArchivosMultipleForm()

    context = {
        'simbolo_form': simbolo_form,
        'archivos_form': archivos_form,
        'titulo': 'Editar Investigacion',
        'modo_edicion': True,
        'simbolo': simbolo,
        'archivos_multimedia': simbolo.multimedia.all()
    }
    return render(request, 'gestion/simbolo_form.html', context)


@user_passes_test(lambda user: user.is_superuser)
def crear_investigador(request):
    if request.method == 'POST':
        form = InvestigadorCreationForm(request.POST)
        if form.is_valid():
            investigador = form.save(commit=False)
            investigador.is_staff = False
            investigador.is_superuser = False
            investigador.save()
            return redirect('gestion:mis_investigaciones')
    else:
        form = InvestigadorCreationForm()

    context = {
        'form': form
    }
    return render(request, 'gestion/crear_investigador.html', context)


def publico_placeholder(request):
    return render(request, 'gestion/publico.html')


@login_required
def logout_usuario(request):
    auth_logout(request)
    return redirect('login')


@user_passes_test(lambda user: user.is_superuser)
def rutas_servidor(request):
    context = {
        'db_path': settings.DATABASES['default']['NAME'],
        'media_root': settings.MEDIA_ROOT,
        'backup_root': settings.BACKUP_ROOT,
    }
    return render(request, 'gestion/rutas.html', context)
