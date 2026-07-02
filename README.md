## Diagrama de clases

```mermaid
graph TD
    subgraph Cliente[Usuario / Navegador]
        Browser[Navegador Web]
    end

    subgraph Django[Proyecto Django - petroglifos_maule]
        subgraph Routing[urls.py - Enrutamiento]
            R1["/ (home_public)"]
            R2["/petroglifo/int/ (publico_detalle)"]
            R3["/mis-investigaciones/ (catalogo_mis)"]
            R4["/catalogo/ (catalogo_todas)"]
            R5["/simbolo/int/ (simbolo_detalle)"]
            R6["/simbolo/nuevo/ (crear_simbolo)"]
            R7["/simbolo/int/editar/ (editar_simbolo)"]
            R8["/investigadores/nuevo/ (crear_investigador)"]
            R9["/rutas/ (rutas_servidor)"]
            R10["/login/ & /logout/ (Django Auth)"]
            R11["/admin/ (Django Admin)"]
        end

        subgraph Views[views.py - Controladores]
            V_Pub["Vistas Públicas<br/>(home_public, publico_detalle)"]
            V_Inv["Vistas Investigadores<br/>(catalogo_mis, catalogo_todas, simbolo_detalle)"]
            V_Ed["Vistas Edición<br/>(crear_simbolo, editar_simbolo)"]
            V_Sup["Vistas Superusuario<br/>(crear_investigador, rutas_servidor)"]
        end

        subgraph Forms[forms.py - Validación de Datos]
            F_Sim["SimboloForm<br/>(Datos del símbolo)"]
            F_Mul["ArchivosMultipleForm<br/>(Carga múltiple de imágenes)"]
            F_User["InvestigadorCreationForm<br/>(Registro de usuarios)"]
        end

        subgraph Templates[Templates - Capa de Presentación]
            T_Base["base.html / base_publica.html<br/>(Plantillas base)"]
            T_Pub["home.html, publico_detalle.html<br/>(Sitio Público)"]
            T_Cat["catalogo.html<br/>(Listado de investigaciones)"]
            T_Det["simbolo_detalle.html<br/>(Detalle de símbolo)"]
            T_Form["simbolo_form.html<br/>(Crear/Editar símbolo)"]
            T_AdminUser["crear_investigador.html, login.html<br/>(Gestión de usuarios)"]
            T_Sys["rutas.html<br/>(Información del sistema)"]
        end

        subgraph Admin[admin.py - Panel de Administración]
            A_Sitio["SitioAdmin + BloqueInline"]
            A_Bloque["BloqueAdmin + PanelInline"]
            A_Panel["PanelAdmin + SimboloInline"]
            A_Sim["SimboloAdmin + ArchivoMultimediaInline<br/>(+ acción 'desactivar_simbolos')"]
            A_Multi["ArchivoMultimediaAdmin<br/>(+ vista_previa en listado)"]
        end

        subgraph Models[models.py - Modelos de Datos]
            M_Sitio[(Sitio)]
            M_Bloque[(Bloque)]
            M_Panel[(Panel)]
            M_Simbolo[(Simbolo)]
            M_Multimedia[(ArchivoMultimedia)]
            M_User[(User - Django)]
        end
    end

    subgraph Storage[Almacenamiento Físico]
        DB[(SQLite / db.sqlite3)]
        Media[Carpeta /media/<br/>Archivos subidos (FOTOs y CALCOs)]
    end

    %% Conexiones de flujo
    Browser --> Routing
    Routing --> Views
    Views --> Forms
    Views --> Templates
    Views --> Models
    Views --> Admin
    Admin --> Models
    Models --> DB
    Models --> Media
    Templates --> Browser
```