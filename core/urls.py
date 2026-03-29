from django.urls import path
from . import views

urlpatterns = [

    # ── PÚBLICO ──────────────────────────────────────────────────────────────
    path('',                    views.raiz,              name='raiz'),
    path('main/',               views.main,              name='main'),
    path('adoptar/',            views.adoptar,           name='adoptar'),
    path('refugios/',           views.refugios_publicos, name='refugios'),
    path('contacto/',           views.contacto,          name='contacto'),
    path('contactenos/',        views.contactenos,       name='contactenos'),

    # ── AUTH ─────────────────────────────────────────────────────────────────
    path('login/',              views.login_view,        name='login'),
    path('logout/',             views.logout_view,       name='logout'),
    path('register/',           views.register,          name='register'),
    path('perfil/',             views.perfil,            name='perfil'),

    # ── BLOG ─────────────────────────────────────────────────────────────────
    path('blog/',               views.blog_lista,        name='blog_lista'),
    path('blog/<int:id>/',      views.blog_detalle,      name='blog_detalle'),

    # ── NOTICIAS ─────────────────────────────────────────────────────────────
    path('noticias/',                           views.noticias_lista,     name='noticias_lista'),
    path('noticias/<int:id>/',                  views.noticia_detalle,    name='noticia_detalle'),
    path('noticias/categoria/<str:categoria>/', views.noticias_categoria, name='noticias_categoria'),

    # ── ADOPTANTE ────────────────────────────────────────────────────────────
    path('adoptante/dashboard/',                    views.adoptante_dashboard,       name='adoptante_dashboard'),
    path('adoptante/mascotas/',                     views.adoptante_mascotas,        name='adoptante_mascotas'),
    path('adoptante/mascotas/<int:id>/',            views.adoptante_mascota_detalle, name='adoptante_mascota_detalle'),
    path('adoptante/adopciones/',                   views.adoptante_mis_adopciones,  name='adoptante_mis_adopciones'),
    path('adoptante/adopciones/<int:id>/',          views.adoptante_adopcion_detalle,name='adoptante_adopcion_detalle'),
    path('adoptante/solicitar/<int:mascota_id>/',   views.adoptante_solicitar,       name='adoptante_solicitar'),
    path('adoptante/perfil/',                       views.adoptante_perfil,          name='adoptante_perfil'),

    # ── REFUGIO ──────────────────────────────────────────────────────────────
    path('refugio/dashboard/',                      views.refugio_dashboard,         name='refugio_dashboard'),
    path('refugio/mascotas/',                       views.refugio_mascotas,          name='refugio_mascotas'),
    path('refugio/mascotas/nueva/',                 views.refugio_mascota_form,      name='refugio_mascota_nueva'),
    path('refugio/mascotas/editar/<int:id>/',       views.refugio_mascota_form,      name='refugio_mascota_editar'),
    path('refugio/mascotas/eliminar/<int:id>/',     views.refugio_mascota_eliminar,  name='refugio_mascota_eliminar'),
    path('refugio/adopciones/',                     views.refugio_adopciones,        name='refugio_adopciones'),
    path('refugio/adopciones/<int:id>/',            views.refugio_adopcion_detalle,  name='refugio_adopcion_detalle'),
    path('refugio/adopciones/aprobar/<int:id>/',    views.refugio_aprobar_adopcion,  name='refugio_aprobar_adopcion'),
    path('refugio/adopciones/rechazar/<int:id>/',   views.refugio_rechazar_adopcion, name='refugio_rechazar_adopcion'),
    path('refugio/perfil/',                         views.refugio_perfil,            name='refugio_perfil'),

    # ── ADMIN ────────────────────────────────────────────────────────────────
    path('admin/dashboard/',                        views.admin_dashboard,              name='admin_dashboard'),

    # mascotas
    path('admin/mascotas/',                         views.admin_mascotas,               name='admin_mascotas'),
    path('admin/mascotas/nueva/',                   views.admin_mascota_form,            name='admin_mascota_nueva'),
    path('admin/mascotas/editar/<int:id>/',         views.admin_mascota_form,            name='admin_mascota_editar'),
    path('admin/mascotas/eliminar/<int:id>/',       views.admin_mascota_eliminar,        name='admin_mascota_eliminar'),

    # adopciones
    path('admin/adopciones/',                       views.admin_adopciones,              name='admin_adopciones'),
    path('admin/adopciones/pendientes/',            views.admin_adopciones_pendientes,   name='admin_adopciones_pendientes'),
    path('admin/adopciones/detalle/<int:id>/',      views.admin_adopcion_detalle,        name='admin_adopcion_detalle'),
    path('admin/adopciones/aprobar/<int:id>/',      views.admin_aprobar_adopcion,        name='admin_aprobar_adopcion'),
    path('admin/adopciones/rechazar/<int:id>/',     views.admin_rechazar_adopcion,       name='admin_rechazar_adopcion'),
    path('admin/adopciones/completar/<int:id>/',    views.admin_completar_adopcion,      name='admin_completar_adopcion'),

    # usuarios
    path('admin/usuarios/',                         views.admin_usuarios,                name='admin_usuarios'),
    path('admin/usuarios/editar/<int:id>/',         views.admin_usuario_editar,          name='admin_usuario_editar'),
    path('admin/usuarios/toggle/<int:id>/',         views.admin_usuario_toggle,          name='admin_usuario_toggle'),
    path('admin/usuarios/resetear/<int:id>/',       views.admin_usuario_resetear_password, name='admin_usuario_resetear_password'),

    # refugios
    path('admin/refugios/',                         views.admin_refugios,                name='admin_refugios'),
    path('admin/refugios/nuevo/',                   views.admin_refugio_form,            name='admin_refugio_nuevo'),
    path('admin/refugios/editar/<int:id>/',         views.admin_refugio_form,            name='admin_refugio_editar'),
    path('admin/refugios/eliminar/<int:id>/',       views.admin_refugio_eliminar,        name='admin_refugio_eliminar'),
    path('admin/refugios/toggle/<int:id>/',         views.admin_refugio_toggle,          name='admin_refugio_toggle'),

    # reportes
    path('admin/reportes/',                         views.admin_reportes,                name='admin_reportes'),
    path('admin/reportes/mascotas/pdf/',            views.reporte_mascotas_pdf,          name='reporte_mascotas_pdf'),
    path('admin/reportes/adopciones/pdf/',          views.reporte_adopciones_pdf,        name='reporte_adopciones_pdf'),
    path('admin/reportes/mascotas/excel/',          views.reporte_mascotas_excel,        name='reporte_mascotas_excel'),
    path('admin/reportes/adopciones/excel/',        views.reporte_adopciones_excel,      name='reporte_adopciones_excel'),

    # ... otras rutas ...
 
    path('dashboard/refugio/', views.refugio_dashboard, name='refugio_dashboard'),
    path('dashboard/adoptante/', views.adoptante_dashboard, name='adoptante_dashboard'),
    path('error404/',           views.error404,          name='error404'),
    path('error/403/',          views.error403,          name='error403'),
]