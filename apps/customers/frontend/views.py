from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from apps.customers.backend.exceptions import (
    ClienteConOperacionesException,
    ClienteDuplicadoException,
    ClienteInactivoException,
    ClienteNoEncontradoException,
    DocumentoInvalidoException,
    LimiteCreditoInvalidoException,
)

from apps.customers.backend.services import CustomerService

from .forms import (
    ClienteCreateForm,
    ClienteUpdateForm,
)


def customer_list(request):
    """Muestra la lista de clientes."""

    clientes = CustomerService.list_clientes()

    return render(
        request,
        "customers/list.html",
        {
            "clientes": clientes,
        },
    )


def cliente_create(request):
    """Crea un cliente."""

    if request.method == "POST":
        form = ClienteCreateForm(request.POST)

        if form.is_valid():
            try:
                CustomerService.create_cliente(
                    tipo_documento=form.cleaned_data[
                        "tipo_documento"
                    ],
                    numero_documento=form.cleaned_data[
                        "numero_documento"
                    ],
                    nombre=form.cleaned_data["nombre"],
                    apellido=form.cleaned_data["apellido"],
                    telefono=form.cleaned_data["telefono"],
                    email=form.cleaned_data["email"],
                    direccion=form.cleaned_data["direccion"],
                    ciudad=form.cleaned_data["ciudad"],
                    departamento=form.cleaned_data[
                        "departamento"
                    ],
                    limite_credito=form.cleaned_data[
                        "limite_credito"
                    ],
                )

            except (
                ClienteDuplicadoException,
                DocumentoInvalidoException,
                LimiteCreditoInvalidoException,
            ) as exc:
                form.add_error(None, str(exc))

            else:
                messages.success(
                    request,
                    "Cliente creado correctamente.",
                )

                return redirect(
                    "customers:list"
                )

    else:
        form = ClienteCreateForm()

    return render(
        request,
        "customers/form.html",
        {
            "form": form,
            "title": "Nuevo cliente",
            "submit_text": "Crear cliente",
        },
    )


def cliente_detail(request, cliente_id):
    """Muestra el detalle de un cliente."""

    try:
        cliente = CustomerService.get_cliente(
            cliente_id
        )

    except ClienteNoEncontradoException as exc:
        raise Http404(str(exc))

    return render(
        request,
        "customers/detail.html",
        {
            "cliente": cliente,
        },
    )


def cliente_update(request, cliente_id):
    """Actualiza los datos permitidos de un cliente."""

    try:
        cliente = CustomerService.get_cliente(
            cliente_id
        )

    except ClienteNoEncontradoException as exc:
        raise Http404(str(exc))

    if request.method == "POST":
        form = ClienteUpdateForm(request.POST)

        if form.is_valid():
            try:
                CustomerService.update_cliente(
                    cliente_id,
                    nombre=form.cleaned_data["nombre"],
                    apellido=form.cleaned_data["apellido"],
                    telefono=form.cleaned_data["telefono"],
                    email=form.cleaned_data["email"],
                    direccion=form.cleaned_data["direccion"],
                    ciudad=form.cleaned_data["ciudad"],
                    departamento=form.cleaned_data[
                        "departamento"
                    ],
                    limite_credito=form.cleaned_data[
                        "limite_credito"
                    ],
                    estado=form.cleaned_data["estado"],
                )

            except ClienteNoEncontradoException as exc:
                raise Http404(str(exc))

            except LimiteCreditoInvalidoException as exc:
                form.add_error(
                    "limite_credito",
                    str(exc),
                )

            else:
                messages.success(
                    request,
                    "Cliente actualizado correctamente.",
                )

                return redirect(
                    "customers:detail",
                    cliente_id=cliente_id,
                )

    else:
        form = ClienteUpdateForm(
            initial={
                "nombre": cliente.nombre,
                "apellido": cliente.apellido,
                "telefono": cliente.telefono,
                "email": cliente.email,
                "direccion": cliente.direccion,
                "ciudad": cliente.ciudad,
                "departamento": cliente.departamento,
                "limite_credito": cliente.limite_credito,
                "estado": cliente.estado,
            }
        )

    return render(
        request,
        "customers/form.html",
        {
            "form": form,
            "cliente": cliente,
            "title": "Editar cliente",
            "submit_text": "Guardar cambios",
        },
    )


def cliente_delete(request, cliente_id):
    """Elimina un cliente cuando las reglas de negocio lo permiten."""

    if request.method != "POST":
        return redirect(
            "customers:detail",
            cliente_id=cliente_id,
        )

    try:
        CustomerService.delete_cliente(
            cliente_id
        )

    except ClienteNoEncontradoException as exc:
        raise Http404(str(exc))

    except ClienteConOperacionesException as exc:
        messages.error(
            request,
            str(exc),
        )

        return redirect(
            "customers:detail",
            cliente_id=cliente_id,
        )

    else:
        messages.success(
            request,
            "Cliente eliminado correctamente.",
        )

        return redirect(
            "customers:list"
        )


def cliente_deactivate(request, cliente_id):
    """Desactiva un cliente."""

    if request.method != "POST":
        return redirect(
            "customers:detail",
            cliente_id=cliente_id,
        )

    try:
        CustomerService.deactivate_cliente(
            cliente_id
        )

    except ClienteNoEncontradoException as exc:
        raise Http404(str(exc))

    else:
        messages.success(
            request,
            "Cliente desactivado correctamente.",
        )

        return redirect(
            "customers:detail",
            cliente_id=cliente_id,
        )


def cliente_activate(request, cliente_id):
    """Activa un cliente."""

    if request.method != "POST":
        return redirect(
            "customers:detail",
            cliente_id=cliente_id,
        )

    try:
        CustomerService.activate_cliente(
            cliente_id
        )

    except ClienteNoEncontradoException as exc:
        raise Http404(str(exc))

    else:
        messages.success(
            request,
            "Cliente activado correctamente.",
        )

        return redirect(
            "customers:detail",
            cliente_id=cliente_id,
        )
