from django.urls import path

from . import views


app_name = "cartera"


urlpatterns = [
    path(
        "",
        views.cartera_list,
        name="list",
    ),
    path(
        "pedidos/",
        views.cartera_pedidos_disponibles,
        name="pedidos_disponibles",
    ),
    path(
        "pedidos/<int:pedido_id>/crear/",
        views.cartera_pedido_create,
        name="pedido_create",
    ),
    path(
        "otras/nueva/",
        views.cartera_otra_create,
        name="otra_create",
    ),
    path(
        "otras/nueva/guardar/",
        views.cartera_otra_create_post,
        name="otra_create_post",
    ),
    path(
        "<int:cartera_id>/",
        views.cartera_detail,
        name="detail",
    ),
    path(
        "<int:cartera_id>/abonos/nuevo/",
        views.abono_create,
        name="abono_create",
    ),
]
