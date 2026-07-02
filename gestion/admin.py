from django.contrib import admin
from django.utils.html import format_html
from .models import Sitio, Bloque, Panel, Simbolo, ArchivoMultimedia

# Clases para mejorar la visualización en el admin
class BloqueInline(admin.TabularInline):
    model = Bloque
    extra = 1  # Muestra 1 campo para añadir un bloque nuevo

class PanelInline(admin.TabularInline):
    model = Panel
    extra = 1

class SimboloInline(admin.TabularInline):
    model = Simbolo
    extra = 1

class ArchivoMultimediaInline(admin.TabularInline):
    model = ArchivoMultimedia
    extra = 1

# Admin principal para Sitio, con los demás anidados
@admin.register(Sitio)
class SitioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'comuna', 'esta_activo')
    list_filter = ('comuna', 'esta_activo')
    search_fields = ('nombre', 'comuna')
    inlines = [BloqueInline]

@admin.register(Bloque)
class BloqueAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'sitio')
    list_filter = ('sitio',)
    search_fields = ('codigo',)
    inlines = [PanelInline]

@admin.register(Panel)
class PanelAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'bloque')
    list_filter = ('bloque__sitio',)
    search_fields = ('codigo',)
    inlines = [SimboloInline]

@admin.register(Simbolo)
class SimboloAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'autor', 'panel', 'iconografia', 'estado_conservacion', 'esta_activo')
    list_filter = ('panel__bloque__sitio', 'autor', 'esta_activo')
    search_fields = ('codigo', 'descripcion', 'iconografia')
    inlines = [ArchivoMultimediaInline]

    actions = ['desactivar_simbolos']

    def desactivar_simbolos(self, request, queryset):
        queryset.update(esta_activo=False)
        self.message_user(request, 'Simbolos desactivados correctamente.')
    desactivar_simbolos.short_description = 'Desactivar simbolos (no eliminar)'

@admin.register(ArchivoMultimedia)
class ArchivoMultimediaAdmin(admin.ModelAdmin):
    list_display = ('vista_previa', 'simbolo', 'autor', 'tipo_archivo', 'es_principal', 'ruta_archivo')
    list_filter = ('tipo_archivo', 'es_principal', 'simbolo__autor', 'simbolo__panel__bloque__sitio')
    search_fields = ('simbolo__codigo', 'simbolo__autor__username')
    ordering = ('simbolo__autor__username', 'simbolo__codigo')
    list_select_related = ('simbolo', 'simbolo__autor', 'simbolo__panel', 'simbolo__panel__bloque', 'simbolo__panel__bloque__sitio')

    def vista_previa(self, obj):
        if obj.archivo and obj.tipo_archivo == 'FOTO':
            return format_html(
                '<img src="{}" style="width: 70px; height: 50px; object-fit: cover; border-radius: 6px;" />',
                obj.archivo.url
            )
        return '-'
    vista_previa.short_description = 'Miniatura'

    def autor(self, obj):
        return obj.simbolo.autor.username if obj.simbolo and obj.simbolo.autor else '-'
    autor.short_description = 'Investigador'

    def ruta_archivo(self, obj):
        return obj.archivo.path if obj.archivo else '-'
    ruta_archivo.short_description = 'Ruta en servidor'
