from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from apps.inventory.backend.exceptions import (
ArticuloConInventarioException,
ArticuloDuplicadoException,
ArticuloInactivoException,
ArticuloNoEncontradoException,
ItemInventarioNoEncontradoException,
SKUInvalidoException,
StockInvalidoException,
)

from apps.inventory.backend.services import InventoryService

from .forms import (
ArticuloCreateForm,
ArticuloUpdateForm,
ItemInventarioForm,
)

def inventory_list(request):
    """Muestra la lista de artículos."""

    articulos = InventoryService.list_articulos()

    return render(
        request,
        "inventory/list.html",
        {
            "articulos": articulos,
        },
    )


def articulo_create(request):
    """Crea un artículo."""


    if request.method == "POST":
        form = ArticuloCreateForm(request.POST)

        if form.is_valid():
            try:
                InventoryService.create_articulo(
                    descripcion=form.cleaned_data["descripcion"],
                    clasificacion=form.cleaned_data["clasificacion"],
                    unidad_medida=form.cleaned_data["unidad_medida"],
                    costo_base=form.cleaned_data["costo_base"],
                    alerta_minimo=form.cleaned_data["alerta_minimo"],
                    ubicacion_almacen=form.cleaned_data[
                        "ubicacion_almacen"
                    ],
                    color=form.cleaned_data["color"],
                )
            except (
                ArticuloDuplicadoException,
                SKUInvalidoException,
            ) as exc:
                form.add_error(None, str(exc))
            else:
                messages.success(
                    request,
                    "Artículo creado correctamente.",
                )
                return redirect("inventory:list")
    else:
        form = ArticuloCreateForm()

    return render(
        request,
        "inventory/form.html",
        {
            "form": form,
            "title": "Nuevo artículo",
            "submit_text": "Crear artículo",
        },
    )


def articulo_detail(request, articulo_id):
    """Muestra el detalle del artículo y su inventario."""


    try:
        articulo = InventoryService.get_articulo(articulo_id)
    except ArticuloNoEncontradoException as exc:
        raise Http404(str(exc))

    stock = InventoryService.get_stock(articulo_id)
    items = InventoryService.get_inventory_items(articulo_id)

    return render(
        request,
        "inventory/detail.html",
        {
            "articulo": articulo,
            "stock": stock,
            "items": items,
            "low_stock": stock < articulo.alerta_minimo,
            "inventory_form": ItemInventarioForm(),
        },
    )


def articulo_update(request, articulo_id):
    """Actualiza los datos permitidos de un artículo."""


    try:
        articulo = InventoryService.get_articulo(articulo_id)
    except ArticuloNoEncontradoException as exc:
        raise Http404(str(exc))

    if request.method == "POST":
        form = ArticuloUpdateForm(request.POST)

        if form.is_valid():
            try:
                InventoryService.update_articulo(
                    articulo_id,
                    costo_base=form.cleaned_data["costo_base"],
                    alerta_minimo=form.cleaned_data[
                        "alerta_minimo"
                    ],
                    ubicacion_almacen=form.cleaned_data[
                        "ubicacion_almacen"
                    ],
                    estado=form.cleaned_data["estado"],
                )
            except ArticuloNoEncontradoException as exc:
                raise Http404(str(exc))
            else:
                messages.success(
                    request,
                    "Artículo actualizado correctamente.",
                )
                return redirect(
                    "inventory:detail",
                    articulo_id=articulo_id,
                )
    else:
        form = ArticuloUpdateForm(
            initial={
                "costo_base": articulo.costo_base,
                "alerta_minimo": articulo.alerta_minimo,
                "ubicacion_almacen": articulo.ubicacion_almacen,
                "estado": articulo.estado,
            }
        )

    return render(
        request,
        "inventory/form.html",
        {
            "form": form,
            "articulo": articulo,
            "title": "Editar artículo",
            "submit_text": "Guardar cambios",
        },
    )

def articulo_delete(request, articulo_id):
    """Elimina un artículo si las reglas de negocio lo permiten."""


    if request.method != "POST":
        return redirect("inventory:detail", articulo_id=articulo_id)

    try:
        InventoryService.delete_articulo(articulo_id)

    except ArticuloNoEncontradoException as exc:
        raise Http404(str(exc))

    except ArticuloConInventarioException as exc:
        messages.error(request, str(exc))
        return redirect(
            "inventory:detail",
            articulo_id=articulo_id,
        )

    else:
        messages.success(
            request,
            "Artículo eliminado correctamente.",
        )
        return redirect("inventory:list")
    

def inventory_add(request, articulo_id):
    """Agrega inventario a un artículo."""


    try:
        articulo = InventoryService.get_articulo(articulo_id)
    except ArticuloNoEncontradoException as exc:
        raise Http404(str(exc))

    if request.method != "POST":
        return redirect(
            "inventory:detail",
            articulo_id=articulo_id,
        )

    form = ItemInventarioForm(request.POST)

    if form.is_valid():
        try:
            InventoryService.add_inventory(
                articulo_id=articulo_id,
                cantidad=form.cleaned_data["cantidad"],
                ubicacion=form.cleaned_data["ubicacion"],
            )

        except ArticuloInactivoException as exc:
            form.add_error(None, str(exc))

        except StockInvalidoException as exc:
            form.add_error("cantidad", str(exc))

        else:
            messages.success(
                request,
                "Inventario agregado correctamente.",
            )

            if request.headers.get("HX-Request"):
                return _inventory_table_response(
                    request,
                    articulo_id,
                )

            return redirect(
                "inventory:detail",
                articulo_id=articulo_id,
            )

    if request.headers.get("HX-Request"):
        return render(
            request,
            "inventory/partials/inventory_form.html",
            {
                "form": form,
                "articulo": articulo,
            },
            status=400,
        )

    return render(
        request,
        "inventory/detail.html",
        {
            "articulo": articulo,
            "stock": InventoryService.get_stock(articulo_id),
            "items": InventoryService.get_inventory_items(
                articulo_id
            ),
            "low_stock": InventoryService.is_low_stock(
                articulo_id
            ),
            "inventory_form": form,
        },
        status=400,
    )


def inventory_update(request, item_id):
    """Actualiza un registro de inventario."""


    if request.method != "POST":
        return redirect("inventory:list")

    try:
        item = InventoryService.get_inventory_item(item_id)
    except ItemInventarioNoEncontradoException as exc:
        raise Http404(str(exc))

    articulo_id = item.articulo_id

    form = ItemInventarioForm(request.POST)

    if form.is_valid():
        try:
            InventoryService.update_inventory(
                item_id=item_id,
                cantidad=form.cleaned_data["cantidad"],
                ubicacion=form.cleaned_data["ubicacion"],
            )

        except ItemInventarioNoEncontradoException as exc:
            raise Http404(str(exc))

        except StockInvalidoException as exc:
            form.add_error("cantidad", str(exc))

        else:
            messages.success(
                request,
                "Inventario actualizado correctamente.",
            )

            if request.headers.get("HX-Request"):
                return _inventory_table_response(
                    request,
                    articulo_id,
                )

            return redirect(
                "inventory:detail",
                articulo_id=articulo_id,
            )

    articulo = InventoryService.get_articulo(articulo_id)

    if request.headers.get("HX-Request"):
        return render(
            request,
            "inventory/partials/inventory_form.html",
            {
                "form": form,
                "articulo": articulo,
                "item": item,
            },
            status=400,
        )

    return render(
        request,
        "inventory/detail.html",
        {
            "articulo": articulo,
            "stock": InventoryService.get_stock(articulo_id),
            "items": InventoryService.get_inventory_items(
                articulo_id
            ),
            "low_stock": InventoryService.is_low_stock(
                articulo_id
            ),
            "inventory_form": form,
        },
        status=400,
    )

def inventory_delete(request, item_id):
    """Elimina un registro de inventario."""

    if request.method != "POST":
        return redirect("inventory:list")

    try:
        item = InventoryService.get_inventory_item(item_id)
    except ItemInventarioNoEncontradoException as exc:
        raise Http404(str(exc))

    articulo_id = item.articulo_id

    try:
        InventoryService.remove_inventory(item_id)
    except ItemInventarioNoEncontradoException as exc:
        raise Http404(str(exc))

    messages.success(
        request,
        "Registro de inventario eliminado correctamente.",
    )

    if request.headers.get("HX-Request"):
        return _inventory_table_response(
            request,
            articulo_id,
        )

    return redirect(
        "inventory:detail",
        articulo_id=articulo_id,
    )

def _inventory_table_response(request, articulo_id):
    """Devuelve la tabla de inventario para HTMX."""

    articulo = InventoryService.get_articulo(articulo_id)

    return render(
        request,
        "inventory/partials/inventory_table.html",
        {
            "articulo": articulo,
            "items": InventoryService.get_inventory_items(
                articulo_id
            ),
            "stock": InventoryService.get_stock(
                articulo_id
            ),
        },
    )
