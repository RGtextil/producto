from decimal import Decimal

from django.db import transaction

from .constants import ClienteEstado
from .exceptions import (
    ClienteConOperacionesException,
    ClienteDuplicadoException,
    ClienteInactivoException,
    ClienteNoEncontradoException,
    DocumentoInvalidoException,
    LimiteCreditoInvalidoException,
)
from .repositories import ClienteRepository


class CustomerService:

    @staticmethod
    def _normalize_text(value):
        return str(value or "").strip()

    @classmethod
    def _normalize_documento(cls, numero_documento):
        documento = cls._normalize_text(numero_documento)

        if not documento:
            raise DocumentoInvalidoException(
                "El número de documento es obligatorio."
            )

        return documento

    @classmethod
    @transaction.atomic
    def create_cliente(
        cls,
        *,
        tipo_documento,
        numero_documento,
        nombre,
        apellido="",
        telefono="",
        email="",
        direccion="",
        ciudad="",
        departamento="",
        limite_credito=0,
    ):
        numero_documento = cls._normalize_documento(
            numero_documento
        )

        nombre = cls._normalize_text(nombre)

        if not nombre:
            raise ClienteDuplicadoException(
                "El nombre del cliente es obligatorio."
            )

        if ClienteRepository.exists_by_documento(
            numero_documento
        ):
            raise ClienteDuplicadoException(
                "Ya existe un cliente con este número de documento."
            )

        limite_credito = Decimal(str(limite_credito))

        if limite_credito < 0:
            raise LimiteCreditoInvalidoException(
                "El límite de crédito no puede ser negativo."
            )

        return ClienteRepository.create(
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
            nombre=nombre,
            apellido=cls._normalize_text(apellido),
            telefono=cls._normalize_text(telefono),
            email=cls._normalize_text(email),
            direccion=cls._normalize_text(direccion),
            ciudad=cls._normalize_text(ciudad),
            departamento=cls._normalize_text(departamento),
            limite_credito=limite_credito,
            estado=ClienteEstado.ACTIVO,
        )

    @staticmethod
    def get_cliente(cliente_id):
        cliente = ClienteRepository.get_by_id(cliente_id)

        if cliente is None:
            raise ClienteNoEncontradoException(
                "El cliente no existe."
            )

        return cliente

    @classmethod
    def get_cliente_by_documento(
        cls,
        tipo_documento,
        numero_documento,
    ):
        numero_documento = cls._normalize_documento(
            numero_documento
        )

        cliente = ClienteRepository.get_by_documento(
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
        )

        if cliente is None:
            raise ClienteNoEncontradoException(
                "El cliente no existe."
            )

        return cliente

    @staticmethod
    def list_clientes():
        return ClienteRepository.list_all()

    @staticmethod
    def list_clientes_activos():
        return ClienteRepository.list_active()

    @staticmethod
    @transaction.atomic
    def update_cliente(
        cliente_id,
        *,
        nombre=None,
        apellido=None,
        telefono=None,
        email=None,
        direccion=None,
        ciudad=None,
        departamento=None,
        limite_credito=None,
        estado=None,
    ):
        cliente = CustomerService.get_cliente(cliente_id)

        data = {}

        if nombre is not None:
            nombre = CustomerService._normalize_text(nombre)

            if not nombre:
                raise ClienteNoEncontradoException(
                    "El nombre del cliente es obligatorio."
                )

            data["nombre"] = nombre

        if apellido is not None:
            data["apellido"] = (
                CustomerService._normalize_text(apellido)
            )

        if telefono is not None:
            data["telefono"] = (
                CustomerService._normalize_text(telefono)
            )

        if email is not None:
            data["email"] = (
                CustomerService._normalize_text(email)
            )

        if direccion is not None:
            data["direccion"] = (
                CustomerService._normalize_text(direccion)
            )

        if ciudad is not None:
            data["ciudad"] = (
                CustomerService._normalize_text(ciudad)
            )

        if departamento is not None:
            data["departamento"] = (
                CustomerService._normalize_text(departamento)
            )

        if limite_credito is not None:
            limite_credito = Decimal(str(limite_credito))

            if limite_credito < 0:
                raise LimiteCreditoInvalidoException(
                    "El límite de crédito no puede ser negativo."
                )

            data["limite_credito"] = limite_credito

        if estado is not None:
            data["estado"] = estado

        if not data:
            return cliente

        return ClienteRepository.update(
            cliente,
            **data,
        )

    @staticmethod
    @transaction.atomic
    def deactivate_cliente(cliente_id):
        cliente = CustomerService.get_cliente(cliente_id)

        if cliente.estado == ClienteEstado.INACTIVO:
            return cliente

        return ClienteRepository.update(
            cliente,
            estado=ClienteEstado.INACTIVO,
        )

    @staticmethod
    @transaction.atomic
    def activate_cliente(cliente_id):
        cliente = CustomerService.get_cliente(cliente_id)

        if cliente.estado == ClienteEstado.ACTIVO:
            return cliente

        return ClienteRepository.update(
            cliente,
            estado=ClienteEstado.ACTIVO,
        )

    @staticmethod
    @transaction.atomic
    def delete_cliente(cliente_id):
        cliente = CustomerService.get_cliente(cliente_id)

        # Actualmente no existen relaciones con otros módulos
        # que permitan determinar operaciones históricas.
        # Esta validación se ampliará cuando Orders/Cartera
        # tengan relación con Cliente.
        ClienteRepository.delete(cliente)

    @staticmethod
    def ensure_cliente_activo(cliente_id):
        cliente = CustomerService.get_cliente(cliente_id)

        if cliente.estado != ClienteEstado.ACTIVO:
            raise ClienteInactivoException(
                "El cliente está inactivo y no puede utilizarse."
            )

        return cliente
