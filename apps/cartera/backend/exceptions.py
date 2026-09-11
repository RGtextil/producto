class CarteraException(Exception):
    """Excepción base del módulo de cartera."""


class CarteraNoEncontradaException(CarteraException):
    """La cartera solicitada no existe."""


class CarteraInvalidaException(CarteraException):
    """La cartera no cumple las reglas de negocio."""


class CarteraDuplicadaException(CarteraException):
    """El pedido ya tiene una cartera asociada."""


class CarteraPedidoInvalidoException(CarteraException):
    """El pedido no puede convertirse en cartera."""


class CarteraPedidoNoEntregadoException(CarteraException):
    """El pedido no está entregado y no puede generar cartera."""


class CarteraTotalInvalidoException(CarteraException):
    """El total de la cartera no es válido."""


class CarteraFechaInvalidaException(CarteraException):
    """Las fechas de la cartera no son válidas."""


class CarteraInactivaException(CarteraException):
    """La cartera no puede recibir operaciones."""


class CarteraPagadaException(CarteraException):
    """La cartera ya está completamente pagada."""


class AbonoNoEncontradoException(CarteraException):
    """El abono solicitado no existe."""


class AbonoInvalidoException(CarteraException):
    """El abono no cumple las reglas de negocio."""


class AbonoExcedeSaldoException(CarteraException):
    """El abono supera el saldo pendiente de la cartera."""


class AbonoMontoInvalidoException(CarteraException):
    """El monto del abono no es válido."""


class AbonoFechaInvalidaException(CarteraException):
    """La fecha del abono no es válida."""