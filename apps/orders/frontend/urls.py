from django.urls import path

from . import views


app_name = "orders"


urlpatterns = [
    path(
        "",
        views.order_list,
        name="list",
    ),
    path(
        "pedidos/nuevo/",
        views.pedido_create,
        name="create",
    ),
    path(
        "pedidos/<int:pedido_id>/",
        views.pedido_detail,
        name="detail",
    ),
]