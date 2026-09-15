from django.urls import path

from . import views


app_name = "balance"


urlpatterns = [
    # ============================================================
    # RESUMEN GENERAL
    # ============================================================

    path(
        "",
        views.balance_detail,
        name="detail",
    ),

    # ============================================================
    # OTROS DINEROS
    # ============================================================

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

    path(
        "otros-dineros/<int:otro_dinero_id>/editar/",
        views.otro_dinero_update,
        name="otro_dinero_update",
    ),

    path(
        "otros-dineros/<int:otro_dinero_id>/eliminar/",
        views.otro_dinero_delete,
        name="otro_dinero_delete",
    ),

    # ============================================================
    # DEUDAS
    # ============================================================

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

    path(
        "deudas/<int:deuda_id>/editar/",
        views.deuda_update,
        name="deuda_update",
    ),

    path(
        "deudas/<int:deuda_id>/eliminar/",
        views.deuda_delete,
        name="deuda_delete",
    ),
]