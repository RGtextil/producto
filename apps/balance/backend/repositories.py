from django.db.models import Sum

from .exceptions import (
    DeudaNoEncontradaException,
    OtroDineroNoEncontradoException,
)
from .models import Deuda, OtroDinero


class OtroDineroRepository:
    @staticmethod
    def get_by_id(otro_dinero_id):
        return (
            OtroDinero.objects
            .filter(pk=otro_dinero_id)
            .first()
        )

    @staticmethod
    def get_required(otro_dinero_id):
        otro_dinero = OtroDineroRepository.get_by_id(otro_dinero_id)

        if otro_dinero is None:
            raise OtroDineroNoEncontradoException(
                "El otro dinero no existe."
            )

        return otro_dinero

    @staticmethod
    def create(**data):
        return OtroDinero.objects.create(**data)

    @staticmethod
    def update(otro_dinero, **data):
        for field, value in data.items():
            setattr(otro_dinero, field, value)

        otro_dinero.save(
            update_fields=[
                *data.keys(),
                "updated_at",
            ]
        )

        return otro_dinero

    @staticmethod
    def list_all():
        return (
            OtroDinero.objects
            .all()
        )

    @staticmethod
    def list_by_tipo(tipo):
        return (
            OtroDinero.objects
            .filter(tipo=tipo)
            .all()
        )

    @staticmethod
    def get_total():
        result = OtroDinero.objects.aggregate(
            total=Sum("monto")
        )

        return result["total"] or 0

    @staticmethod
    def delete(otro_dinero):
        otro_dinero.delete()


class DeudaRepository:
    @staticmethod
    def get_by_id(deuda_id):
        return (
            Deuda.objects
            .filter(pk=deuda_id)
            .first()
        )

    @staticmethod
    def get_required(deuda_id):
        deuda = DeudaRepository.get_by_id(deuda_id)

        if deuda is None:
            raise DeudaNoEncontradaException(
                "La deuda no existe."
            )

        return deuda

    @staticmethod
    def create(**data):
        return Deuda.objects.create(**data)

    @staticmethod
    def update(deuda, **data):
        for field, value in data.items():
            setattr(deuda, field, value)

        deuda.save(
            update_fields=[
                *data.keys(),
                "updated_at",
            ]
        )

        return deuda

    @staticmethod
    def list_all():
        return (
            Deuda.objects
            .all()
        )

    @staticmethod
    def list_by_tipo(tipo):
        return (
            Deuda.objects
            .filter(tipo=tipo)
            .all()
        )

    @staticmethod
    def get_total():
        result = Deuda.objects.aggregate(
            total=Sum("monto")
        )

        return result["total"] or 0

    @staticmethod
    def delete(deuda):
        deuda.delete()