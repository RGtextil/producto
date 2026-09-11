from .exceptions import ClienteNoEncontradoException
from .models import Cliente


class ClienteRepository:
    @staticmethod
    def get_by_id(cliente_id):
        return (
            Cliente.objects
            .filter(pk=cliente_id)
            .first()
        )

    @staticmethod
    def get_by_documento(tipo_documento, numero_documento):
        return (
            Cliente.objects
            .filter(
                tipo_documento=tipo_documento,
                numero_documento=numero_documento,
            )
            .first()
        )

    @staticmethod
    def exists_by_documento(numero_documento):
        return Cliente.objects.filter(
            numero_documento=numero_documento,
        ).exists()

    @staticmethod
    def create(**data):
        return Cliente.objects.create(**data)

    @staticmethod
    def update(cliente, **data):
        for field, value in data.items():
            setattr(cliente, field, value)

        cliente.save(
            update_fields=[
                *data.keys(),
                "updated_at",
            ]
        )

        return cliente

    @staticmethod
    def list_all():
        return Cliente.objects.all()

    @staticmethod
    def list_active():
        return (
            Cliente.objects
            .filter(estado="ACTIVO")
        )

    @staticmethod
    def delete(cliente):
        cliente.delete()

    @staticmethod
    def get_required(cliente_id):
        cliente = ClienteRepository.get_by_id(cliente_id)

        if cliente is None:
            raise ClienteNoEncontradoException(
                "El cliente no existe."
            )

        return cliente
