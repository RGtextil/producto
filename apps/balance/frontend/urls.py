from django.urls import path

from . import views


app_name = "balance"


urlpatterns = [
    # Resumen general
    path(
        "",
        views.balance_detail,
        name="detail",
    ),

    # Otros dineros
    path(
        "otros-dineros/",
        views.otro_dinero_list,
        name="otro_dinero_list",
    ),
    path(
        "otros-dineros/nuevo/",
        views.otro_dinero_create,
        name="otro_dinero_create",
    ),
    path(
        "otros-dineros/<int:otro_dinero_id>/",
        views.otro_dinero_detail,
        name="otro_dinero_detail",
    ),

    # Deudas
    path(
        "deudas/",
        views.deuda_list,
        name="deuda_list",
    ),
    path(
        "deudas/nueva/",
        views.deuda_create,
        name="deuda_create",
    ),
    path(
        "deudas/<int:deuda_id>/",
        views.deuda_detail,
        name="deuda_detail",
    ),
]