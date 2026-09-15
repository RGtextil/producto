from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from apps.balance.backend.exceptions import (
    DeudaFechaInvalidaException,
    DeudaFechaVencimientoInvalidaException,
    DeudaInvalidaException,
    DeudaMontoInvalidoException,
    DeudaNoEncontradaException,
    OtroDineroFechaInvalidaException,
    OtroDineroInvalidoException,
    OtroDineroMontoInvalidoException,
    OtroDineroNoEncontradoException,
)
from apps.balance.backend.services import BalanceService
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from .forms import DeudaForm, OtroDineroForm


@require_GET
def balance_detail(request):
    resumen = BalanceService.get_resumen()

    return render(
        request,
        "balance/detail.html",
        {
            "resumen": resumen,
            "otros_dineros": BalanceService.list_otros_dineros(),
            "deudas": BalanceService.list_deudas(),
        },
    )


@require_GET
def otro_dinero_list(request):
    return render(
        request,
        "balance/otros_dineros/list.html",
        {
            "otros_dineros": BalanceService.list_otros_dineros(),
        },
    )


@require_http_methods(["GET", "POST"])
def otro_dinero_create(request):
    if request.method == "GET":
        form = OtroDineroForm()

        return render(
            request,
            "balance/otros_dineros/form.html",
            {"form": form},
        )

    form = OtroDineroForm(request.POST)

    if not form.is_valid():
        return render(
            request,
            "balance/otros_dineros/form.html",
            {"form": form},
            status=400,
        )

    try:
        BalanceService.create_otro_dinero(
            nombre=form.cleaned_data["nombre"],
            tipo=form.cleaned_data["tipo"],
            concepto=form.cleaned_data["concepto"],
            monto=form.cleaned_data["monto"],
            fecha=form.cleaned_data["fecha"],
        )

    except (
        OtroDineroInvalidoException,
        OtroDineroMontoInvalidoException,
        OtroDineroFechaInvalidaException,
    ) as exc:
        form.add_error(None, str(exc))

        return render(
            request,
            "balance/otros_dineros/form.html",
            {"form": form},
            status=400,
        )

    messages.success(
        request,
        "El otro dinero se registró correctamente.",
    )

    return redirect("balance:detail")


@require_GET
def otro_dinero_detail(request, otro_dinero_id):
    try:
        otro_dinero = BalanceService.get_otro_dinero(
            otro_dinero_id
        )

    except OtroDineroNoEncontradoException as exc:
        messages.error(request, str(exc))
        return redirect("balance:otro_dinero_list")

    return render(
        request,
        "balance/otros_dineros/detail.html",
        {
            "otro_dinero": otro_dinero,
        },
    )


@require_GET
def deuda_list(request):
    return render(
        request,
        "balance/deudas/list.html",
        {
            "deudas": BalanceService.list_deudas(),
        },
    )


@require_http_methods(["GET", "POST"])
def deuda_create(request):
    if request.method == "GET":
        form = DeudaForm()

        return render(
            request,
            "balance/deudas/form.html",
            {"form": form},
        )

    form = DeudaForm(request.POST)

    if not form.is_valid():
        return render(
            request,
            "balance/deudas/form.html",
            {"form": form},
            status=400,
        )

    try:
        BalanceService.create_deuda(
            nombre=form.cleaned_data["nombre"],
            tipo=form.cleaned_data["tipo"],
            concepto=form.cleaned_data["concepto"],
            monto=form.cleaned_data["monto"],
            fecha=form.cleaned_data["fecha"],
            fecha_vencimiento=form.cleaned_data[
                "fecha_vencimiento"
            ],
        )

    except (
        DeudaInvalidaException,
        DeudaMontoInvalidoException,
        DeudaFechaInvalidaException,
        DeudaFechaVencimientoInvalidaException,
    ) as exc:
        form.add_error(None, str(exc))

        return render(
            request,
            "balance/deudas/form.html",
            {"form": form},
            status=400,
        )

    messages.success(
        request,
        "La deuda se registró correctamente.",
    )

    return redirect("balance:detail")


@require_GET
def deuda_detail(request, deuda_id):
    try:
        deuda = BalanceService.get_deuda(deuda_id)

    except DeudaNoEncontradaException as exc:
        messages.error(request, str(exc))
        return redirect("balance:deuda_list")

    return render(
        request,
        "balance/deudas/detail.html",
        {
            "deuda": deuda,
        },
    )

@require_http_methods(["GET", "POST"])
def otro_dinero_update(request, otro_dinero_id):
    try:
        otro_dinero = BalanceService.get_otro_dinero(
            otro_dinero_id
        )

    except OtroDineroNoEncontradoException as exc:
        messages.error(request, str(exc))
        return redirect("balance:otro_dinero_list")

    if request.method == "GET":
        form = OtroDineroForm(
            initial={
                "nombre": otro_dinero.nombre,
                "tipo": otro_dinero.tipo,
                "concepto": otro_dinero.concepto,
                "monto": otro_dinero.monto,
                "fecha": otro_dinero.fecha,
            }
        )

        return render(
            request,
            "balance/otros_dineros/form.html",
            {
                "form": form,
                "otro_dinero": otro_dinero,
                "modo_edicion": True,
            },
        )

    form = OtroDineroForm(request.POST)

    if not form.is_valid():
        return render(
            request,
            "balance/otros_dineros/form.html",
            {
                "form": form,
                "otro_dinero": otro_dinero,
                "modo_edicion": True,
            },
            status=400,
        )

    try:
        BalanceService.update_otro_dinero(
            otro_dinero_id,
            nombre=form.cleaned_data["nombre"],
            tipo=form.cleaned_data["tipo"],
            concepto=form.cleaned_data["concepto"],
            monto=form.cleaned_data["monto"],
            fecha=form.cleaned_data["fecha"],
        )

    except (
        OtroDineroInvalidoException,
        OtroDineroMontoInvalidoException,
        OtroDineroFechaInvalidaException,
    ) as exc:
        form.add_error(None, str(exc))

        return render(
            request,
            "balance/otros_dineros/form.html",
            {
                "form": form,
                "otro_dinero": otro_dinero,
                "modo_edicion": True,
            },
            status=400,
        )

    messages.success(
        request,
        "El otro dinero se actualizó correctamente.",
    )

    return redirect("balance:detail")


@require_POST
def otro_dinero_delete(request, otro_dinero_id):
    try:
        BalanceService.delete_otro_dinero(
            otro_dinero_id
        )

    except OtroDineroNoEncontradoException as exc:
        messages.error(request, str(exc))
        return redirect("balance:otro_dinero_list")

    messages.success(
        request,
        "El otro dinero se eliminó correctamente.",
    )

    return redirect("balance:detail")


@require_http_methods(["GET", "POST"])
def deuda_update(request, deuda_id):
    try:
        deuda = BalanceService.get_deuda(
            deuda_id
        )

    except DeudaNoEncontradaException as exc:
        messages.error(request, str(exc))
        return redirect("balance:deuda_list")

    if request.method == "GET":
        form = DeudaForm(
            initial={
                "nombre": deuda.nombre,
                "tipo": deuda.tipo,
                "concepto": deuda.concepto,
                "monto": deuda.monto,
                "fecha": deuda.fecha,
                "fecha_vencimiento": deuda.fecha_vencimiento,
            }
        )

        return render(
            request,
            "balance/deudas/form.html",
            {
                "form": form,
                "deuda": deuda,
                "modo_edicion": True,
            },
        )

    form = DeudaForm(request.POST)

    if not form.is_valid():
        return render(
            request,
            "balance/deudas/form.html",
            {
                "form": form,
                "deuda": deuda,
                "modo_edicion": True,
            },
            status=400,
        )

    try:
        BalanceService.update_deuda(
            deuda_id,
            nombre=form.cleaned_data["nombre"],
            tipo=form.cleaned_data["tipo"],
            concepto=form.cleaned_data["concepto"],
            monto=form.cleaned_data["monto"],
            fecha=form.cleaned_data["fecha"],
            fecha_vencimiento=form.cleaned_data[
                "fecha_vencimiento"
            ],
        )

    except (
        DeudaInvalidaException,
        DeudaMontoInvalidoException,
        DeudaFechaInvalidaException,
        DeudaFechaVencimientoInvalidaException,
    ) as exc:
        form.add_error(None, str(exc))

        return render(
            request,
            "balance/deudas/form.html",
            {
                "form": form,
                "deuda": deuda,
                "modo_edicion": True,
            },
            status=400,
        )

    messages.success(
        request,
        "La deuda se actualizó correctamente.",
    )

    return redirect("balance:detail")


@require_POST
def deuda_delete(request, deuda_id):
    try:
        BalanceService.delete_deuda(
            deuda_id
        )

    except DeudaNoEncontradaException as exc:
        messages.error(request, str(exc))
        return redirect("balance:deuda_list")

    messages.success(
        request,
        "La deuda se eliminó correctamente.",
    )

    return redirect("balance:detail")