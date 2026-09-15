from decimal import Decimal

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from apps.customers.backend.services import CustomerService
from apps.inventory.backend.exceptions import (
    ArticuloNoEncontradoException,
)
from apps.inventory.backend.services import InventoryService
from apps.orders.backend.services import OrderService

from .forms import (
    PedidoArticuloForm,
    PedidoClienteForm,
)

def _get_productos_sesion(request):

    productos_sesion = request.session.get(
        "pedido_productos",
        [],
    )

    productos = []
    total = Decimal("0")

    for producto in productos_sesion:

        cantidad = Decimal(
            str(producto["cantidad"])
        )

        precio_venta = Decimal(
            str(producto["precio_venta"])
        )

        subtotal = cantidad * precio_venta

        productos.append(
            {
                "articulo_id": producto["articulo_id"],
                "sku": producto["sku"],
                "descripcion": producto["descripcion"],
                "color": producto["color"],
                "cantidad": cantidad,
                "precio_venta": precio_venta,
                "subtotal": subtotal,
            }
        )

        total += subtotal

    return productos, total

@require_GET
def pedido_list(request):
    """
    Lista los pedidos existentes.

    Solo lectura.
    La consulta se realiza mediante OrderService.
    """

    pedidos = OrderService.list_pedidos()

    return render(
        request,
        "orders/list.html",
        {
            "pedidos": pedidos,
        },
    )

@require_GET
def pedido_create(request):

    productos, total = _get_productos_sesion(request)

    form = PedidoArticuloForm()

    cliente_form = PedidoClienteForm()

    clientes = CustomerService.list_clientes_activos()

    descripciones = (
        InventoryService
        .list_descripciones_disponibles()
    )

    return render(
        request,
        "orders/form.html",
        {
            "form": form,
            "cliente_form": cliente_form,
            "clientes": clientes,
            "descripciones": descripciones,
            "productos": productos,
            "total": total,
            "title": "Nuevo pedido",
        },
    )

@require_POST
def pedido_agregar_producto(request):

    form = PedidoArticuloForm(request.POST)

    if not form.is_valid():

        productos, total = _get_productos_sesion(request)

        clientes = CustomerService.list_clientes_activos()

        descripciones = (
            InventoryService
            .list_descripciones_disponibles()
        )

        cliente_form = PedidoClienteForm()

        return render(
            request,
            "orders/form.html",
            {
                "form": form,
                "cliente_form": cliente_form,
                "clientes": clientes,
                "descripciones": descripciones,
                "productos": productos,
                "total": total,
                "title": "Nuevo pedido",
            },
            status=400,
        )

    descripcion = form.cleaned_data["descripcion"]
    color = form.cleaned_data["color"]

    try:

        articulo = (
            InventoryService
            .get_articulo_by_descripcion_and_color(
                descripcion,
                color,
            )
        )

    except ArticuloNoEncontradoException as exc:

        form.add_error(
            "color",
            str(exc),
        )

        productos, total = _get_productos_sesion(request)

        clientes = CustomerService.list_clientes_activos()

        descripciones = (
            InventoryService
            .list_descripciones_disponibles()
        )

        cliente_form = PedidoClienteForm()

        return render(
            request,
            "orders/form.html",
            {
                "form": form,
                "cliente_form": cliente_form,
                "clientes": clientes,
                "descripciones": descripciones,
                "productos": productos,
                "total": total,
                "title": "Nuevo pedido",
            },
            status=400,
        )

    producto = {
        "articulo_id": articulo.id,
        "sku": articulo.sku,
        "descripcion": articulo.descripcion,
        "color": articulo.color,
        "cantidad": str(
            form.cleaned_data["cantidad"]
        ),
        "precio_venta": str(
            form.cleaned_data["precio_venta"]
        ),
    }

    productos_sesion = request.session.get(
        "pedido_productos",
        [],
    )

    productos_sesion.append(producto)

    request.session["pedido_productos"] = productos_sesion
    request.session.modified = True

    messages.success(
        request,
        "Producto agregado al pedido.",
    )

    return redirect(
        "orders:create"
    )

@require_POST
def pedido_eliminar_producto(request, index):

    productos_sesion = request.session.get(
        "pedido_productos",
        [],
    )

    try:
        product_index = int(index)

    except (TypeError, ValueError):

        messages.error(
            request,
            "El producto seleccionado no es válido.",
        )

        return redirect(
            "orders:create"
        )

    if (
        product_index < 0
        or product_index >= len(productos_sesion)
    ):

        messages.error(
            request,
            "El producto seleccionado no existe.",
        )

        return redirect(
            "orders:create"
        )

    productos_sesion.pop(product_index)

    request.session["pedido_productos"] = productos_sesion
    request.session.modified = True

    messages.success(
        request,
        "Producto eliminado del pedido.",
    )

    return redirect(
        "orders:create"
    )

@require_POST
def pedido_crear(request):
    """
    Crea definitivamente el pedido.

    Los productos ya fueron agregados previamente
    y se encuentran temporalmente en la sesión.

    Esta vista NO utiliza PedidoArticuloForm.
    """

    productos, total = _get_productos_sesion(request)

    # -----------------------------------------------------
    # VALIDAR QUE EXISTAN PRODUCTOS
    # -----------------------------------------------------

    if not productos:

        messages.error(
            request,
            "El pedido debe contener al menos un producto.",
        )

        return redirect(
            "orders:create"
        )

    # -----------------------------------------------------
    # VALIDAR CLIENTE
    # -----------------------------------------------------

    cliente_form = PedidoClienteForm(
        request.POST
    )

    if not cliente_form.is_valid():

        clientes = (
            CustomerService
            .list_clientes_activos()
        )

        descripciones = (
            InventoryService
            .list_descripciones_disponibles()
        )

        form = PedidoArticuloForm()

        return render(
            request,
            "orders/form.html",
            {
                "form": form,
                "cliente_form": cliente_form,
                "clientes": clientes,
                "descripciones": descripciones,
                "productos": productos,
                "total": total,
                "title": "Nuevo pedido",
            },
            status=400,
        )

    # -----------------------------------------------------
    # OBTENER CLIENTE
    # -----------------------------------------------------

    cliente_id = (
        cliente_form.cleaned_data[
            "cliente_id"
        ]
    )

    # -----------------------------------------------------
    # RECONSTRUIR ITEMS
    # -----------------------------------------------------
    #
    # Los datos vienen de la sesión, pero el
    # OrderService vuelve a validar todo en backend.
    #

    items = [
        {
            "articulo_id": producto["articulo_id"],
            "cantidad": producto["cantidad"],
            "precio_venta": producto["precio_venta"],
        }
        for producto in productos
    ]

    # -----------------------------------------------------
    # CREAR PEDIDO
    # -----------------------------------------------------

    pedido = OrderService.create_pedido(
        cliente_id=cliente_id,
        items=items,
    )

    # -----------------------------------------------------
    # LIMPIAR BORRADOR
    # -----------------------------------------------------

    request.session.pop(
        "pedido_productos",
        None,
    )

    request.session.modified = True

    # -----------------------------------------------------
    # MENSAJE
    # -----------------------------------------------------

    messages.success(
        request,
        f"Pedido #{pedido.id} creado correctamente.",
    )

    # -----------------------------------------------------
    # REDIRECCIÓN
    # -----------------------------------------------------

    return redirect(
        "orders:list"
    )


@require_GET
def pedido_colores(request):
    """
    Devuelve los colores disponibles para una descripción.

    Solo lectura.
    Diseñada para ser consumida por HTMX.
    """

    descripcion = request.GET.get(
        "descripcion",
        "",
    ).strip()

    colores = (
        InventoryService
        .list_colores_by_descripcion(
            descripcion
        )
    )

    return render(
        request,
        "orders/partials/color_options.html",
        {
            "descripcion": descripcion,
            "colores": colores,
        },
    )

@require_GET
def pedido_articulo(request):
    """
    Identifica un artículo mediante descripción y color.

    Solo lectura.
    Diseñada para ser consumida por HTMX.
    """

    descripcion = request.GET.get(
        "descripcion",
        "",
    ).strip()

    color = request.GET.get(
        "color",
        "",
    ).strip()

    # -----------------------------------------------------
    # DATOS INCOMPLETOS
    # -----------------------------------------------------

    if not descripcion or not color:

        return render(
            request,
            "orders/partials/articulo_selected.html",
            {
                "articulo": None,
            },
        )

    # -----------------------------------------------------
    # BUSCAR ARTÍCULO
    # -----------------------------------------------------

    try:

        articulo = (
            InventoryService
            .get_articulo_by_descripcion_and_color(
                descripcion,
                color,
            )
        )

    except ArticuloNoEncontradoException:

        articulo = None

    # -----------------------------------------------------
    # RESPUESTA HTMX
    # -----------------------------------------------------

    return render(
        request,
        "orders/partials/articulo_selected.html",
        {
            "articulo": articulo,
        },
    )