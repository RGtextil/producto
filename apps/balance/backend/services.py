from datetime import date
from decimal import Decimal

from django.db import transaction
from apps.cartera.backend.services import CarteraService
from apps.inventory.backend.repositories import ItemInventarioRepository

from .constants import DeudaTipo, OtroDineroTipo
from .exceptions import (
    BalanceFechaInvalidaException,
    BalanceMontoInvalidoException,
    DeudaFechaInvalidaException,
    DeudaFechaVencimientoInvalidaException,
    DeudaInvalidaException,
    DeudaMontoInvalidoException,
    OtroDineroFechaInvalidaException,
    OtroDineroInvalidoException,
    OtroDineroMontoInvalidoException,
)
from .repositories import DeudaRepository, OtroDineroRepository

class BalanceService:
    """
    Servicio principal del módulo Balance.

    El balance se calcula siempre a partir de los datos actuales
    de Inventario, Cartera, OtrosDineros y Deudas.
    """

    # ============================================================
    # INVENTARIO
    # ============================================================

   
    @staticmethod
    def get_total_inventario():
        return ItemInventarioRepository.get_total_valor_inventario()
        # ============================================================
    # CARTERA
    # ============================================================

    
    @staticmethod
    def get_saldo_cartera():
        return CarteraService.get_saldo_total()
    # ============================================================
    # OTROS DINEROS
    # ============================================================

    @staticmethod
    def get_otro_dinero(otro_dinero_id):
        return OtroDineroRepository.get_required(otro_dinero_id)

    @staticmethod
    def list_otros_dineros():
        return OtroDineroRepository.list_all()

    @staticmethod
    def list_otros_dineros_by_tipo(tipo):
        return OtroDineroRepository.list_by_tipo(tipo)

    @staticmethod
    def _validate_otro_dinero(
        nombre,
        concepto,
        monto,
        fecha,
    ):
        nombre = str(nombre or "").strip()
        concepto = str(concepto or "").strip()

        if not nombre:
            raise OtroDineroInvalidoException(
                "El nombre del otro dinero es obligatorio."
            )

        if not concepto:
            raise OtroDineroInvalidoException(
                "El concepto del otro dinero es obligatorio."
            )

        try:
            monto = Decimal(str(monto))
        except (TypeError, ValueError):
            raise OtroDineroMontoInvalidoException(
                "El monto del otro dinero no es válido."
            )

        if monto <= 0:
            raise OtroDineroMontoInvalidoException(
                "El monto del otro dinero debe ser mayor que cero."
            )

        if fecha is None:
            raise OtroDineroFechaInvalidaException(
                "La fecha del otro dinero es obligatoria."
            )

        if fecha > date.today():
            raise OtroDineroFechaInvalidaException(
                "La fecha del otro dinero no puede ser futura."
            )

        return nombre, concepto, monto

    @classmethod
    @transaction.atomic
    def create_otro_dinero(
        cls,
        *,
        nombre,
        tipo,
        concepto,
        monto,
        fecha,
    ):
        nombre, concepto, monto = cls._validate_otro_dinero(
            nombre,
            concepto,
            monto,
            fecha,
        )

        if tipo not in OtroDineroTipo.values:
            raise OtroDineroInvalidoException(
                "El tipo de otro dinero no es válido."
            )

        return OtroDineroRepository.create(
            nombre=nombre,
            tipo=tipo,
            concepto=concepto,
            monto=monto,
            fecha=fecha,
        )

    @staticmethod
    @transaction.atomic
    def update_otro_dinero(
        otro_dinero_id,
        *,
        nombre,
        tipo,
        concepto,
        monto,
        fecha,
    ):
        otro_dinero = OtroDineroRepository.get_required(
            otro_dinero_id
        )

        nombre = str(nombre or "").strip()
        concepto = str(concepto or "").strip()

        if not nombre:
            raise OtroDineroInvalidoException(
                "El nombre del otro dinero es obligatorio."
            )

        if not concepto:
            raise OtroDineroInvalidoException(
                "El concepto del otro dinero es obligatorio."
            )

        try:
            monto = Decimal(str(monto))
        except (TypeError, ValueError):
            raise OtroDineroMontoInvalidoException(
                "El monto del otro dinero no es válido."
            )

        if monto <= 0:
            raise OtroDineroMontoInvalidoException(
                "El monto del otro dinero debe ser mayor que cero."
            )

        if fecha is None:
            raise OtroDineroFechaInvalidaException(
                "La fecha del otro dinero es obligatoria."
            )

        if fecha > date.today():
            raise OtroDineroFechaInvalidaException(
                "La fecha del otro dinero no puede ser futura."
            )

        if tipo not in OtroDineroTipo.values:
            raise OtroDineroInvalidoException(
                "El tipo de otro dinero no es válido."
            )

        return OtroDineroRepository.update(
            otro_dinero,
            nombre=nombre,
            tipo=tipo,
            concepto=concepto,
            monto=monto,
            fecha=fecha,
        )

    @staticmethod
    def get_total_otros_dineros():
        return OtroDineroRepository.get_total()

    # ============================================================
    # DEUDAS
    # ============================================================

    @staticmethod
    def get_deuda(deuda_id):
        return DeudaRepository.get_required(deuda_id)

    @staticmethod
    def list_deudas():
        return DeudaRepository.list_all()

    @staticmethod
    def list_deudas_by_tipo(tipo):
        return DeudaRepository.list_by_tipo(tipo)

    @staticmethod
    def _validate_deuda(
        nombre,
        concepto,
        monto,
        fecha,
        fecha_vencimiento,
    ):
        nombre = str(nombre or "").strip()
        concepto = str(concepto or "").strip()

        if not nombre:
            raise DeudaInvalidaException(
                "El nombre de la deuda es obligatorio."
            )

        if not concepto:
            raise DeudaInvalidaException(
                "El concepto de la deuda es obligatorio."
            )

        try:
            monto = Decimal(str(monto))
        except (TypeError, ValueError):
            raise DeudaMontoInvalidoException(
                "El monto de la deuda no es válido."
            )

        if monto <= 0:
            raise DeudaMontoInvalidoException(
                "El monto de la deuda debe ser mayor que cero."
            )

        if fecha is None:
            raise DeudaFechaInvalidaException(
                "La fecha de la deuda es obligatoria."
            )

        if fecha > date.today():
            raise DeudaFechaInvalidaException(
                "La fecha de la deuda no puede ser futura."
            )

        if (
            fecha_vencimiento is not None
            and fecha_vencimiento < fecha
        ):
            raise DeudaFechaVencimientoInvalidaException(
                "La fecha de vencimiento no puede ser anterior "
                "a la fecha de la deuda."
            )

        return nombre, concepto, monto

    @classmethod
    @transaction.atomic
    def create_deuda(
        cls,
        *,
        nombre,
        tipo,
        concepto,
        monto,
        fecha,
        fecha_vencimiento=None,
    ):
        nombre, concepto, monto = cls._validate_deuda(
            nombre,
            concepto,
            monto,
            fecha,
            fecha_vencimiento,
        )

        if tipo not in DeudaTipo.values:
            raise DeudaInvalidaException(
                "El tipo de deuda no es válido."
            )

        return DeudaRepository.create(
            nombre=nombre,
            tipo=tipo,
            concepto=concepto,
            monto=monto,
            fecha=fecha,
            fecha_vencimiento=fecha_vencimiento,
        )

    @classmethod
    @transaction.atomic
    def update_deuda(
        cls,
        deuda_id,
        *,
        nombre,
        tipo,
        concepto,
        monto,
        fecha,
        fecha_vencimiento=None,
    ):
        deuda = DeudaRepository.get_required(deuda_id)

        nombre, concepto, monto = cls._validate_deuda(
            nombre,
            concepto,
            monto,
            fecha,
            fecha_vencimiento,
        )

        if tipo not in DeudaTipo.values:
            raise DeudaInvalidaException(
                "El tipo de deuda no es válido."
            )

        return DeudaRepository.update(
            deuda,
            nombre=nombre,
            tipo=tipo,
            concepto=concepto,
            monto=monto,
            fecha=fecha,
            fecha_vencimiento=fecha_vencimiento,
        )

    @staticmethod
    def get_total_deudas():
        return DeudaRepository.get_total()

    # ============================================================
    # RESUMEN DEL BALANCE
    # ============================================================

    @classmethod
    def get_resumen(cls):
        """
        Calcula el balance financiero actual.

        Activos:
            Inventario
            + Cartera
            + Otros dineros

        Menos:
            Deudas

        Resultado:
            Balance final
        """

        total_inventario = cls.get_total_inventario()
        saldo_cartera = cls.get_saldo_cartera()
        total_otros_dineros = cls.get_total_otros_dineros()
        total_deudas = cls.get_total_deudas()

        balance_final = (
            total_inventario
            + saldo_cartera
            + total_otros_dineros
            - total_deudas
        )

        return {
            "total_inventario": total_inventario,
            "saldo_cartera": saldo_cartera,
            "total_otros_dineros": total_otros_dineros,
            "total_deudas": total_deudas,
            "balance_final": balance_final,
        }


    @staticmethod
    @transaction.atomic
    def delete_otro_dinero(otro_dinero_id):
        otro_dinero = OtroDineroRepository.get_required(
            otro_dinero_id
        )

        OtroDineroRepository.delete(otro_dinero)


    @staticmethod
    @transaction.atomic
    def delete_deuda(deuda_id):
        deuda = DeudaRepository.get_required(
            deuda_id
        )

        DeudaRepository.delete(deuda)     