from django.urls import path

from . import views


app_name = "orders"


urlpatterns = [

    path(
        "pedidos/",
        views.pedido_list,
        name="list",
    ),

    path(
        "pedidos/nuevo/",
        views.pedido_create,
        name="create",
    ),

    path(
        "pedidos/nuevo/agregar/",
        views.pedido_agregar_producto,
        name="agregar_producto",
    ),

    path(
        "pedidos/nuevo/eliminar/<int:index>/",
        views.pedido_eliminar_producto,
        name="eliminar_producto",
    ),
    path(
        "pedidos/nuevo/crear/",
        views.pedido_crear,
        name="crear",
    ),

    path(
        "pedidos/nuevo/colores/",
        views.pedido_colores,
        name="colores",
    ),

    path(
        "pedidos/nuevo/articulo/",
        views.pedido_articulo,
        name="articulo",
    ),
]
