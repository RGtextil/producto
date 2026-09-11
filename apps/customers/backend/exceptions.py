class CustomerException(Exception):
    """Excepción base del módulo de clientes."""


class ClienteException(CustomerException):
    """Error relacionado con un cliente."""


class ClienteDuplicadoException(ClienteException):
    """El cliente ya existe."""


class ClienteNoEncontradoException(ClienteException):
    """El cliente solicitado no existe."""


class ClienteInactivoException(ClienteException):
    """El cliente está inactivo y no puede utilizarse."""


class ClienteConOperacionesException(ClienteException):
    """El cliente tiene operaciones asociadas y no puede eliminarse."""


class DocumentoInvalidoException(ClienteException):
    """El documento del cliente no cumple las reglas establecidas."""


class LimiteCreditoInvalidoException(ClienteException):
    """El límite de crédito del cliente no es válido."""
