class BalanceException(Exception):
    """Excepción base del módulo balance."""


class BalanceInvalidoException(BalanceException):
    """El balance o alguno de sus valores no es válido."""


class BalanceMontoInvalidoException(BalanceException):
    """El monto registrado no es válido."""


class BalanceFechaInvalidaException(BalanceException):
    """La fecha registrada no es válida."""


class OtroDineroNoEncontradoException(BalanceException):
    """El otro dinero solicitado no existe."""


class OtroDineroInvalidoException(BalanceException):
    """Los datos del otro dinero no son válidos."""


class OtroDineroMontoInvalidoException(BalanceException):
    """El monto del otro dinero no es válido."""


class OtroDineroFechaInvalidaException(BalanceException):
    """La fecha del otro dinero no es válida."""


class DeudaNoEncontradaException(BalanceException):
    """La deuda solicitada no existe."""


class DeudaInvalidaException(BalanceException):
    """Los datos de la deuda no son válidos."""


class DeudaMontoInvalidoException(BalanceException):
    """El monto de la deuda no es válido."""


class DeudaFechaInvalidaException(BalanceException):
    """La fecha de la deuda no es válida."""


class DeudaFechaVencimientoInvalidaException(BalanceException):
    """La fecha de vencimiento de la deuda no es válida."""