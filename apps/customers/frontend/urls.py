from django.urls import path

from . import views


app_name = "customers"


urlpatterns = [
    path(
        "",
        views.customer_list,
        name="list",
    ),
    path(
        "clientes/nuevo/",
        views.cliente_create,
        name="create",
    ),
    path(
        "clientes/<int:cliente_id>/",
        views.cliente_detail,
        name="detail",
    ),
    path(
        "clientes/<int:cliente_id>/editar/",
        views.cliente_update,
        name="update",
    ),
    path(
        "clientes/<int:cliente_id>/eliminar/",
        views.cliente_delete,
        name="delete",
    ),
    path(
        "clientes/<int:cliente_id>/desactivar/",
        views.cliente_deactivate,
        name="deactivate",
    ),
    path(
        "clientes/<int:cliente_id>/activar/",
        views.cliente_activate,
        name="activate",
    ),
]
