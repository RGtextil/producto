from django.db.models import Sum

from .exceptions import (
    AbonoNoEncontradoException,
    CarteraNoEncontradaException,
)
from .models import Abono, Cartera


class CarteraRepository:

    @staticmethod
    def get_by_id(cartera_id):
        return (
            Cartera.objects
            .select_related(
                "pedido",
                "pedido__cliente",
            )
            .filter(pk=cartera_id)
            .first()
        )

    @staticmethod
    def get_required(cartera_id):
        cartera = CarteraRepository.get_by_id(cartera_id)

        if cartera is None:
            raise CarteraNoEncontradaException(
                "La cartera no existe."
            )

        return cartera

    @staticmethod
    def get_by_pedido(pedido):
        return (
            Cartera.objects
            .select_related(
                "pedido",
                "pedido__cliente",
            )
            .filter(pedido=pedido)
            .first()
        )

    @staticmethod
    def exists_by_pedido(pedido):
        return Cartera.objects.filter(
            pedido=pedido,
        ).exists()

    @staticmethod
    def create(**data):
        return Cartera.objects.create(**data)

    @staticmethod
    def update(cartera, **data):
        for field, value in data.items():
            setattr(cartera, field, value)

        cartera.save(
            update_fields=[
                *data.keys(),
                "updated_at",
            ]
        )

        return cartera

    @staticmethod
    def list_all():
        return (
            Cartera.objects
            .select_related(
                "pedido",
                "pedido__cliente",
            )
            .prefetch_related("abonos")
            .all()
        )

    @staticmethod
    def list_by_estado(estado):
        return (
            Cartera.objects
            .filter(estado=estado)
            .select_related(
                "pedido",
                "pedido__cliente",
            )
            .prefetch_related("abonos")
            .all()
        )

    @staticmethod
    def list_by_tipo(tipo):
        return (
            Cartera.objects
            .filter(tipo=tipo)
            .select_related(
                "pedido",
                "pedido__cliente",
            )
            .prefetch_related("abonos")
            .all()
        )

    @staticmethod
    def delete(cartera):
        cartera.delete()

    @staticmethod
    def get_total_carteras():
        result = Cartera.objects.aggregate(
            total=Sum("total"),
        )

        return result["total"] or 0


class AbonoRepository:

    @staticmethod
    def get_by_id(abono_id):
        return (
            Abono.objects
            .select_related(
                "cartera",
                "cartera__pedido",
                "cartera__pedido__cliente",
            )
            .filter(pk=abono_id)
            .first()
        )

    @staticmethod
    def get_required(abono_id):
        abono = AbonoRepository.get_by_id(abono_id)

        if abono is None:
            raise AbonoNoEncontradoException(
                "El abono no existe."
            )

        return abono

    @staticmethod
    def create(**data):
        return Abono.objects.create(**data)

    @staticmethod
    def update(abono, **data):
        for field, value in data.items():
            setattr(abono, field, value)

        abono.save(
            update_fields=[
                *data.keys(),
            ]
        )

        return abono

    @staticmethod
    def get_total_abonos():
        result = (
            Abono.objects
            .aggregate(total=Sum("monto"))
        )
        return result["total"] or 0

    @staticmethod
    def list_by_cartera(cartera):
        return (
            Abono.objects
            .filter(cartera=cartera)
            .order_by("-fecha", "-id")
        )

    @staticmethod
    def get_total_by_cartera(cartera):
        result = (
            Abono.objects
            .filter(cartera=cartera)
            .aggregate(
                total=Sum("monto"),
            )
        )

        return result["total"] or 0

    @staticmethod
    def delete(abono):
        abono.delete()