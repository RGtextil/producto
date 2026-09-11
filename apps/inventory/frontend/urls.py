from django.urls import path

from . import views


app_name = "inventory"


urlpatterns = [
    path("", views.inventory_list, name="list"),

    path(
        "articulos/nuevo/",
        views.articulo_create,
        name="create",
    ),

    path(
        "articulos/<int:articulo_id>/",
        views.articulo_detail,
        name="detail",
    ),

    path(
        "articulos/<int:articulo_id>/editar/",
        views.articulo_update,
        name="update",
    ),

    path(
        "articulos/<int:articulo_id>/eliminar/",
        views.articulo_delete,
        name="delete",
    ),

    path(
        "articulos/<int:articulo_id>/inventario/agregar/",
        views.inventory_add,
        name="inventory_add",
    ),

    path(
        "inventario/<int:item_id>/actualizar/",
        views.inventory_update,
        name="inventory_update",
    ),

    path(
        "inventario/<int:item_id>/eliminar/",
        views.inventory_delete,
        name="inventory_delete",
    ),
]