from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from apps.cartera.backend.exceptions import (
    AbonoExcedeSaldoException,
    AbonoFechaInvalidaException,
    AbonoMontoInvalidoException,
    CarteraDuplicadaException,
    CarteraFechaInvalidaException,
    CarteraInvalidaException,
    CarteraNoEncontradaException,
    CarteraPagadaException,
    CarteraPedidoInvalidoException,
    CarteraPedidoNoEntregadoException,
    CarteraTotalInvalidoException,
)
from apps.cartera.backend.services import CarteraService

from .forms import (
    AbonoForm,
    CarteraOtraForm,
    CarteraPedidoForm,
)


@require_GET
def cartera_list(request):
    """
    Listado principal de carteras y resumen general.
    """
    carteras = CarteraService.list_carteras()

    total_carteras = CarteraService.get_total_carteras()
    total_abonos = CarteraService.get_total_abonos_global()
    saldo_total = CarteraService.get_saldo_total()

    return render(
        request,
        "cartera/list.html",
        {
            "carteras": carteras,
            "total_carteras": total_carteras,
            "total_abonos": total_abonos,
            "saldo_total": saldo_total,
        },
    )


@require_GET
def cartera_detail(request, cartera_id):
    """
    Detalle de una cartera y sus abonos.
    """
    try:
        cartera = CarteraService.get_cartera(cartera_id)
    except CarteraNoEncontradaException as exc:
        messages.error(request, str(exc))
        return redirect("cartera:list")

    abonos = CarteraService.list_abonos(cartera_id)
    total_abonos = CarteraService.get_total_abonos(cartera_id)
    saldo = CarteraService.get_saldo(cartera_id)

    abono_form = AbonoForm()

    return render(
        request,
        "cartera/detail.html",
        {
            "cartera": cartera,
            "abonos": abonos,
            "total_abonos": total_abonos,
            "saldo": saldo,
            "abono_form": abono_form,
        },
    )


@require_GET
def cartera_pedidos_disponibles(request):
    """
    Pedidos entregados que todavía no tienen cartera.
    """
    pedidos = CarteraService.list_pedidos_disponibles()

    return render(
        request,
        "cartera/pedidos_disponibles.html",
        {
            "pedidos": pedidos,
        },
    )


@require_http_methods(["GET", "POST"])
def cartera_pedido_create(request, pedido_id):
    """
    Crear una cartera a partir de un pedido ENTREGADO.
    """
    try:
        pedido = CarteraService.get_pedido_para_cartera(pedido_id)
    except (
        CarteraPedidoInvalidoException,
        CarteraPedidoNoEntregadoException,
        CarteraDuplicadaException,
        CarteraTotalInvalidoException,
    ) as exc:
        messages.error(request, str(exc))
        return redirect("cartera:pedidos_disponibles")

    if request.method == "GET":
        form = CarteraPedidoForm()

        return render(
            request,
            "cartera/pedido_form.html",
            {
                "form": form,
                "pedido": pedido,
            },
        )

    form = CarteraPedidoForm(request.POST)

    if not form.is_valid():
        return render(
            request,
            "cartera/pedido_form.html",
            {
                "form": form,
                "pedido": pedido,
            },
            status=400,
        )

    try:
        cartera = CarteraService.create_from_pedido(
            pedido_id=pedido_id,
            fecha_inicio=form.cleaned_data["fecha_inicio"],
            fecha_vencimiento=form.cleaned_data["fecha_vencimiento"],
            concepto=form.cleaned_data["concepto"],
        )
    except (
        CarteraPedidoInvalidoException,
        CarteraPedidoNoEntregadoException,
        CarteraDuplicadaException,
        CarteraFechaInvalidaException,
        CarteraTotalInvalidoException,
        CarteraInvalidaException,
    ) as exc:
        form.add_error(None, str(exc))

        return render(
            request,
            "cartera/pedido_form.html",
            {
                "form": form,
                "pedido": pedido,
            },
            status=400,
        )

    messages.success(
        request,
        "La cartera del pedido se creó correctamente.",
    )

    return redirect(
        "cartera:detail",
        cartera_id=cartera.id,
    )


@require_GET
def cartera_otra_create(request):
    """
    Formulario para crear una cartera manual.
    """
    form = CarteraOtraForm()

    return render(
        request,
        "cartera/otra_form.html",
        {
            "form": form,
        },
    )


@require_POST
def cartera_otra_create_post(request):
    """
    Procesa la creación de una cartera manual.
    """
    form = CarteraOtraForm(request.POST)

    if not form.is_valid():
        return render(
            request,
            "cartera/otra_form.html",
            {
                "form": form,
            },
            status=400,
        )

    try:
        cartera = CarteraService.create_other(
            nombre=form.cleaned_data["nombre"],
            concepto=form.cleaned_data["concepto"],
            fecha_inicio=form.cleaned_data["fecha_inicio"],
            fecha_vencimiento=form.cleaned_data["fecha_vencimiento"],
            total=form.cleaned_data["total"],
        )
    except (
        CarteraInvalidaException,
        CarteraFechaInvalidaException,
        CarteraTotalInvalidoException,
    ) as exc:
        form.add_error(None, str(exc))

        return render(
            request,
            "cartera/otra_form.html",
            {
                "form": form,
            },
            status=400,
        )

    messages.success(
        request,
        "La cartera se creó correctamente.",
    )

    return redirect(
        "cartera:detail",
        cartera_id=cartera.id,
    )


@require_POST
def abono_create(request, cartera_id):
    """
    Registra un abono sobre una cartera.
    """
    try:
        cartera = CarteraService.get_cartera(cartera_id)
    except CarteraNoEncontradaException as exc:
        messages.error(request, str(exc))
        return redirect("cartera:list")

    form = AbonoForm(request.POST)

    if not form.is_valid():
        abonos = CarteraService.list_abonos(cartera_id)
        total_abonos = CarteraService.get_total_abonos(cartera_id)
        saldo = CarteraService.get_saldo(cartera_id)

        return render(
            request,
            "cartera/detail.html",
            {
                "cartera": cartera,
                "abonos": abonos,
                "total_abonos": total_abonos,
                "saldo": saldo,
                "abono_form": form,
            },
            status=400,
        )

    try:
        CarteraService.create_abono(
            cartera_id=cartera_id,
            monto=form.cleaned_data["monto"],
            fecha=form.cleaned_data["fecha"],
            concepto=form.cleaned_data["concepto"],
        )
    except (
        CarteraPagadaException,
        AbonoExcedeSaldoException,
        AbonoMontoInvalidoException,
        AbonoFechaInvalidaException,
    ) as exc:
        form.add_error(None, str(exc))

        abonos = CarteraService.list_abonos(cartera_id)
        total_abonos = CarteraService.get_total_abonos(cartera_id)
        saldo = CarteraService.get_saldo(cartera_id)

        return render(
            request,
            "cartera/detail.html",
            {
                "cartera": cartera,
                "abonos": abonos,
                "total_abonos": total_abonos,
                "saldo": saldo,
                "abono_form": form,
            },
            status=400,
        )

    messages.success(
        request,
        "El abono se registró correctamente.",
    )

    return redirect(
        "cartera:detail",
        cartera_id=cartera_id,
    )