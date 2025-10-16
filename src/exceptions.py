class CalcError(Exception):
    """Базовые ошибки калькулятора"""
    pass

class EmptyStringError(CalcError):
    """Ошибка пустой строки"""
    pass

class UnknownTokenError(CalcError):
    """Ошибка неизвестного токена"""
    pass

class IntegerNumbersError(CalcError):
    """Ошибка - требуются целые числа для оператора"""
    pass

class NotEnoughNumbersError(CalcError):
    """Ошибка недостатка чисел для оператора"""
    pass

class IncorrectExpressionError(CalcError):
    """Ошибка некорректного RPN выражения"""
    pass

class InvalidTokenValueError(CalcError):
    """Ошибка некорректного значения токена"""
