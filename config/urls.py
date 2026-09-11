from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        include("apps.authentication.frontend.urls"),
    ),
    path(
        "inventory/",
        include("apps.inventory.frontend.urls"),
    ),
    path(
        "customers/",
        include("apps.customers.frontend.urls"),
    ),
    path(
        "orders/",
        include("apps.orders.frontend.urls"),
    ),
    path(
        "cartera/",
        include("apps.cartera.frontend.urls"),
    ),
    path(
        "balance/",
        include("apps.balance.frontend.urls"),
    ),
]