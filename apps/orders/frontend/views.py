from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from apps.orders.backend.exceptions import (
    ArticuloInactivoException,
    ArticuloNoEncontradoException,
    CantidadInvalidaException,
    CambioEstadoInvalidoException,
    ClienteInactivoException,
    ClienteNoEncontradoException,
    PedidoItemInvalidoException,
    PedidoNoEncontradoException,
    PedidoSinItemsException,
    PedidoYaEntregadoException,
    PrecioVentaInvalidoException,
    ProductoDuplicadoException,
    StockInsuficienteException,
)

from apps.orders.backend.services import OrderService

from .forms import (
    PedidoForm,
    PedidoItemForm,
)


def order_list(request):
    """Muestra la lista de pedidos."""

    pedidos = OrderService.list_pedidos()

    return render(
        request,
        "orders/list.html",
        {
            "pedidos": pedidos,
        },
    )


def pedido_create(request):
    """Crea un pedido con uno o varios productos."""

    if request.method == "POST":
        form = PedidoForm(request.POST)

        if form.is_valid():
            articulo_ids = request.POST.getlist("articulo")
            cantidades = request.POST.getlist("cantidad")
            precios_venta = request.POST.getlist("precio_venta")

            if not articulo_ids:
                form.add_error(
                    None,
                    "El pedido debe contener al menos un producto.",
                )

            elif not (
                len(articulo_ids)
                == len(cantidades)
                == len(precios_venta)
            ):
                form.add_error(
                    None,
                    "Los datos de los productos del pedido no son válidos.",
                )

            else:
                items = []

                for articulo_id, cantidad, precio_venta in zip(
                    articulo_ids,
                    cantidades,
                    precios_venta,
                ):
                    items.append(
                        {
                            "articulo_id": articulo_id,
                            "cantidad": cantidad,
                            "precio_venta": precio_venta,
                        }
                    )

                try:
                    pedido = OrderService.create_pedido(
                        cliente_id=form.cleaned_data["cliente"].id,
                        items=items,
                    )

                except (
                    ClienteNoEncontradoException,
                    ClienteInactivoException,
                    ArticuloNoEncontradoException,
                    ArticuloInactivoException,
                    CantidadInvalidaException,
                    PrecioVentaInvalidoException,
                    ProductoDuplicadoException,
                    PedidoSinItemsException,
                    PedidoItemInvalidoException,
                    StockInsuficienteException,
                ) as exc:
                    form.add_error(None, str(exc))

                else:
                    messages.success(
                        request,
                        f"Pedido #{pedido.id} creado correctamente.",
                    )

                    return redirect(
                        "orders:detail",
                        pedido_id=pedido.id,
                    )
    else:
        form = PedidoForm()

    item_form = PedidoItemForm()

    return render(
        request,
        "orders/form.html",
        {
            "form": form,
            "item_form": item_form,
            "title": "Nuevo pedido",
            "submit_text": "Crear pedido",
        },
    )


def pedido_detail(request, pedido_id):
    """Muestra el detalle de un pedido."""

    try:
        pedido = OrderService.get_pedido(pedido_id)

    except PedidoNoEncontradoException as exc:
        raise Http404(str(exc))

    items = OrderService.get_items(pedido_id)

    total = OrderService.get_total(pedido_id)

    return render(
        request,
        "orders/detail.html",
        {
            "pedido": pedido,
            "items": items,
            "total": total,
        },
    )


def pedido_cancel(request, pedido_id):
    """
    Intenta cancelar un pedido.

    Actualmente un pedido entregado no puede cancelarse
    automáticamente porque ya produjo movimientos de inventario.
    """

    if request.method != "POST":
        return redirect(
            "orders:detail",
            pedido_id=pedido_id,
        )

    try:
        OrderService.cancel_pedido(pedido_id)

    except PedidoNoEncontradoException as exc:
        raise Http404(str(exc))

    except CambioEstadoInvalidoException as exc:
        messages.error(
            request,
            str(exc),
        )

        return redirect(
            "orders:detail",
            pedido_id=pedido_id,
        )

    else:
        messages.success(
            request,
            "Pedido cancelado correctamente.",
        )

        return redirect(
            "orders:detail",
            pedido_id=pedido_id,
        )


def pedido_deliver(request, pedido_id):
    """
    Intenta entregar un pedido.

    La creación actual ya genera pedidos ENTREGADOS,
    por lo que esta transición queda restringida.
    """

    if request.method != "POST":
        return redirect(
            "orders:detail",
            pedido_id=pedido_id,
        )

    try:
        OrderService.deliver_pedido(pedido_id)

    except PedidoNoEncontradoException as exc:
        raise Http404(str(exc))

    except PedidoYaEntregadoException as exc:
        messages.info(
            request,
            str(exc),
        )

        return redirect(
            "orders:detail",
            pedido_id=pedido_id,
        )

    except CambioEstadoInvalidoException as exc:
        messages.error(
            request,
            str(exc),
        )

        return redirect(
            "orders:detail",
            pedido_id=pedido_id,
        )

    else:
        messages.success(
            request,
            "Pedido entregado correctamente.",
        )

        return redirect(
            "orders:detail",
            pedido_id=pedido_id,
        )
