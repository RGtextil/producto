from datetime import date
from decimal import Decimal

from django.db import transaction

from apps.orders.backend.constants import PedidoEstado
from apps.orders.backend.repositories import PedidoRepository

from .constants import CarteraEstado, CarteraTipo
from .exceptions import (
    AbonoExcedeSaldoException,
    AbonoFechaInvalidaException,
    AbonoInvalidoException,
    AbonoMontoInvalidoException,
    AbonoNoEncontradoException,
    CarteraDuplicadaException,
    CarteraFechaInvalidaException,
    CarteraInvalidaException,
    CarteraNoEncontradaException,
    CarteraPagadaException,
    CarteraPedidoInvalidoException,
    CarteraPedidoNoEntregadoException,
    CarteraTotalInvalidoException,
)
from .repositories import (
    AbonoRepository,
    CarteraRepository,
)


class CarteraService:

    # ---------------------------------------------------------
    # CARTERAS
    # ---------------------------------------------------------

    @staticmethod
    def get_cartera(cartera_id):
        return CarteraRepository.get_required(cartera_id)

    @staticmethod
    def list_carteras():
        return CarteraRepository.list_all()

    @staticmethod
    def list_carteras_pendientes():
        return CarteraRepository.list_by_estado(
            CarteraEstado.PENDIENTE,
        )

    @staticmethod
    def list_carteras_pagadas():
        return CarteraRepository.list_by_estado(
            CarteraEstado.PAGADA,
        )

    @staticmethod
    def list_carteras_pedido():
        return CarteraRepository.list_by_tipo(
            CarteraTipo.PEDIDO,
        )

    @staticmethod
    def list_carteras_otras():
        return CarteraRepository.list_by_tipo(
            CarteraTipo.OTRA,
        )

    @staticmethod
    def _validate_dates(
        fecha_inicio,
        fecha_vencimiento,
    ):
        if fecha_inicio is None:
            raise CarteraFechaInvalidaException(
                "La fecha de inicio es obligatoria."
            )

        if fecha_vencimiento is not None:
            if fecha_vencimiento < fecha_inicio:
                raise CarteraFechaInvalidaException(
                    "La fecha de vencimiento no puede ser "
                    "anterior a la fecha de inicio."
                )

    @staticmethod
    def _validate_total(total):
        try:
            total = Decimal(str(total))
        except (TypeError, ValueError):
            raise CarteraTotalInvalidoException(
                "El total de la cartera no es válido."
            )

        if total <= 0:
            raise CarteraTotalInvalidoException(
                "El total de la cartera debe ser mayor que cero."
            )

        return total

    # ---------------------------------------------------------
    # PEDIDOS DISPONIBLES PARA CARTERA
    # ---------------------------------------------------------

    @staticmethod
    def list_pedidos_disponibles():
        """
        Devuelve únicamente pedidos ENTREGADOS que todavía
        no tienen una cartera asociada.
        """

        pedidos = PedidoRepository.list_by_estado(
            PedidoEstado.ENTREGADO,
        )

        return [
            pedido
            for pedido in pedidos
            if not CarteraRepository.exists_by_pedido(pedido)
        ]

    @staticmethod
    def get_pedido_para_cartera(pedido_id):
        """
        Obtiene un pedido y valida que pueda convertirse
        en cartera.
        """

        pedido = PedidoRepository.get_by_id(pedido_id)

        if pedido is None:
            raise CarteraPedidoInvalidoException(
                "El pedido no existe."
            )

        if pedido.estado != PedidoEstado.ENTREGADO:
            raise CarteraPedidoNoEntregadoException(
                "Solo los pedidos entregados pueden "
                "generar una cartera."
            )

        if CarteraRepository.exists_by_pedido(pedido):
            raise CarteraDuplicadaException(
                "Este pedido ya tiene una cartera asociada."
            )

        if pedido.total <= 0:
            raise CarteraTotalInvalidoException(
                "El pedido no tiene un total válido para generar cartera."
            )

        return pedido

    # ---------------------------------------------------------
    # CREAR CARTERA DESDE PEDIDO
    # ---------------------------------------------------------

    @classmethod
    @transaction.atomic
    def create_from_pedido(
        cls,
        *,
        pedido_id,
        fecha_inicio,
        fecha_vencimiento=None,
        concepto="Venta a crédito",
    ):
        pedido = cls.get_pedido_para_cartera(
            pedido_id,
        )

        cls._validate_dates(
            fecha_inicio,
            fecha_vencimiento,
        )

        total = cls._validate_total(
            pedido.total,
        )

        if not concepto or not str(concepto).strip():
            raise CarteraInvalidaException(
                "El concepto de la cartera es obligatorio."
            )

        nombre = (
            f"Pedido #{pedido.id} - "
            f"{pedido.cliente}"
        )

        return CarteraRepository.create(
            pedido=pedido,
            tipo=CarteraTipo.PEDIDO,
            nombre=nombre,
            concepto=str(concepto).strip(),
            fecha_inicio=fecha_inicio,
            fecha_vencimiento=fecha_vencimiento,
            total=total,
            estado=CarteraEstado.PENDIENTE,
        )

    # ---------------------------------------------------------
    # OTRAS CARTERAS
    # ---------------------------------------------------------

    @classmethod
    @transaction.atomic
    def create_other(
        cls,
        *,
        nombre,
        concepto,
        fecha_inicio,
        fecha_vencimiento=None,
        total,
    ):
        nombre = str(nombre or "").strip()
        concepto = str(concepto or "").strip()

        if not nombre:
            raise CarteraInvalidaException(
                "El nombre de la cartera es obligatorio."
            )

        if not concepto:
            raise CarteraInvalidaException(
                "El concepto de la cartera es obligatorio."
            )

        cls._validate_dates(
            fecha_inicio,
            fecha_vencimiento,
        )

        total = cls._validate_total(total)

        return CarteraRepository.create(
            pedido=None,
            tipo=CarteraTipo.OTRA,
            nombre=nombre,
            concepto=concepto,
            fecha_inicio=fecha_inicio,
            fecha_vencimiento=fecha_vencimiento,
            total=total,
            estado=CarteraEstado.PENDIENTE,
        )

    # ---------------------------------------------------------
    # ABONOS
    # ---------------------------------------------------------

    @staticmethod
    def get_abono(abono_id):
        return AbonoRepository.get_required(abono_id)

    @staticmethod
    def list_abonos(cartera_id):
        cartera = CarteraRepository.get_required(
            cartera_id,
        )

        return AbonoRepository.list_by_cartera(
            cartera,
        )

    @staticmethod
    def get_total_abonos(cartera_id):
        cartera = CarteraRepository.get_required(
            cartera_id,
        )

        return AbonoRepository.get_total_by_cartera(
            cartera,
        )

    @classmethod
    def get_saldo(cls, cartera_id):
        cartera = CarteraRepository.get_required(
            cartera_id,
        )

        total_abonos = AbonoRepository.get_total_by_cartera(
            cartera,
        )

        return max(
            cartera.total - total_abonos,
            Decimal("0"),
        )

    @staticmethod
    def _validate_abono_monto(monto):
        try:
            monto = Decimal(str(monto))
        except (TypeError, ValueError):
            raise AbonoMontoInvalidoException(
                "El monto del abono no es válido."
            )

        if monto <= 0:
            raise AbonoMontoInvalidoException(
                "El monto del abono debe ser mayor que cero."
            )

        return monto

    @staticmethod
    def _validate_abono_fecha(fecha):
        if fecha is None:
            raise AbonoFechaInvalidaException(
                "La fecha del abono es obligatoria."
            )

        if fecha > date.today():
            raise AbonoFechaInvalidaException(
                "La fecha del abono no puede ser futura."
            )

    # ---------------------------------------------------------
    # REGISTRAR ABONO
    # ---------------------------------------------------------

    @classmethod
    @transaction.atomic
    def create_abono(
        cls,
        *,
        cartera_id,
        monto,
        fecha,
        concepto="",
    ):
        cartera = CarteraRepository.get_required(
            cartera_id,
        )

        if cartera.estado == CarteraEstado.PAGADA:
            raise CarteraPagadaException(
                "La cartera ya está completamente pagada."
            )

        cls._validate_abono_fecha(fecha)

        monto = cls._validate_abono_monto(
            monto,
        )

        saldo = cls.get_saldo(
            cartera_id,
        )

        if monto > saldo:
            raise AbonoExcedeSaldoException(
                "El abono no puede superar el saldo pendiente."
            )

        concepto = str(concepto or "").strip()

        abono = AbonoRepository.create(
            cartera=cartera,
            monto=monto,
            fecha=fecha,
            concepto=concepto,
        )

        nuevo_saldo = saldo - monto

        if nuevo_saldo == 0:
            CarteraRepository.update(
                cartera,
                estado=CarteraEstado.PAGADA,
            )

        return abono

    # ---------------------------------------------------------
    # ELIMINAR ABONO
    # ---------------------------------------------------------

    @classmethod
    @transaction.atomic
    def delete_abono(cls, abono_id):
        abono = AbonoRepository.get_required(
            abono_id,
        )

        cartera = abono.cartera

        if cartera.estado == CarteraEstado.PAGADA:
            raise AbonoInvalidoException(
                "No se puede eliminar un abono de una "
                "cartera que ya está pagada."
            )

        AbonoRepository.delete(
            abono,
        )

    # ---------------------------------------------------------
    # TOTALES GENERALES
    # ---------------------------------------------------------
    @staticmethod
    def get_total_abonos_global():
        return AbonoRepository.get_total_abonos()

    @staticmethod
    def get_total_carteras():
        return CarteraRepository.get_total_carteras()

    @staticmethod
    def get_total_abonos(cartera_id):
        cartera = CarteraRepository.get_required(cartera_id)
        return AbonoRepository.get_total_by_cartera(cartera)

    @classmethod
    def get_saldo_total(cls):
        total_carteras = cls.get_total_carteras()
        total_abonos = cls.get_total_abonos_global()

        return max(
            total_carteras - total_abonos,
            Decimal("0"),
        )