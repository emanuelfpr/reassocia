from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("projetos/<int:id>/", views.projeto, name="projeto"),
    path("consulta/", views.consulta, name="consulta"),
    path("contato/", views.contato, name="contato"),
    path("sobre/", views.sobre, name="sobre"),

    path("login/", views.entrar, name="login"),
    path("logout/", views.sair, name="logout"),

    path("admin/projetos/", views.admin_lista, name="admin_lista"),
    path("admin/projetos/novo/", views.admin_novo, name="admin_novo"),
    path("admin/projetos/<int:id>/editar/", views.admin_editar, name="admin_editar"),
]
