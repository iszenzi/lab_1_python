import re
from src.constants import OPERATIONS
from src.exceptions import (
    UnknownTokenError,
    EmptyStringError,
    NotEnoughNumbersError,
    IncorrectExpressionError,
    IntegerNumbersError,
    InvalidTokenValueError
)

def token_type(part: str) -> tuple[str, int | float | None]:
    """
    Распределяет токены на конкретные виды
    :param part: Часть строки, разбитая регулярное выражение
    :return: Возвращает кортеж, где первый элемент это тип токена, второй элемент - значение токена
    """
    #Добавление токена целого числа
    if part.isdigit():
        return ("NUMBER", int(part))
    #Добавление токена оператора
    elif part in OPERATIONS:
        return (part, None)
    else:
        try:
            # Пробуем преобразовать в float и добавить токен вещественного числа
            return ("NUMBER", float(part))
        except ValueError:
            # Если не число и не оператор - ошибка
            raise UnknownTokenError(f'Неизвестный токен "{part}"')

def tokenize2(string: str) -> list[tuple[str, float | int | None]]:
    """
    Разбивает строку на токены: числа и операторы
    Кладет полученные токены в список
    Для целого числа кладем в список ('NUMBER', int())
    Для вещественного числа кладем в список ('NUMBER', float())
    Для оператора кладем в список ('Оператор', None)
    :param string: RPN выражение, записанное пользователем
    :return: Возвращает список токенов
    """
    tokens: list[tuple[str, float | int | None]] = []
    #Проверка на пустую строку
    if not string.split():
        raise EmptyStringError('Введена пустая строка')
    joined_string = "".join(string.split())
    #Регулярное выражение, задающее токены
    pattern = r'\s*([+\-]?\d+(?:\.\d+)?|//|\*\*|[%+\-*/])'
    joined_tokens = "".join(re.findall(pattern, string))
    #Преобразование токенов в конкретные виды
    tokens = [token_type(token) for token in re.findall(pattern, string)]
    #Проверка, что пользователь ввел корректные токены
    if joined_tokens == joined_string:
        return tokens
    #Нахождение неизвестных токенов
    else:
        for i in joined_tokens:
            joined_string = joined_string.replace(i, ' ')
        invalid_token = joined_string
        raise UnknownTokenError(f'Неизвестный токен "{invalid_token}"')

def calculate(tokens: list[tuple[str, float | int | None]]) -> float | int:
    """
    Вычисляет значение RPN выражения
    :param tokens: список токенов, полученных из tokenize()
    :return: Возвращает результат вычисления RPN выражения
    """
    stack: list[float | int] = []
    operations = OPERATIONS
    for token_type, token_value in tokens:
        #Добавление числа в стек
        if token_type == 'NUMBER':
            if token_value is None:
                raise InvalidTokenValueError("Токен числа не может быть значения None")
            stack.append(token_value)
        #Проверка возможности выполнения операции
        elif token_type in operations:
            if len(stack) < 2:
                raise NotEnoughNumbersError(f'Недостаточно чисел для оператора "{token_type}"')
            b = stack.pop() #второе число
            a = stack.pop() #первое число
            #Проверка деления на 0
            if token_type in ['/', '//', '%'] and b == 0:
                raise ZeroDivisionError('Деление на ноль')
            #Для операторов // и % числа должны быть целыми
            if token_type in ['//', '%']:
                if (a % 1 == 0) + (b % 1 == 0) != 2:
                    raise IntegerNumbersError(f'Для операции "{token_type}" нужны целые числа')
                else:
                    stack.append(operations[token_type](a, b))
            if token_type in ['+', '-', '*', '**']:
                stack.append(operations[token_type](a, b))
        else:
            raise UnknownTokenError(f'Неизвестный токен "{token_type}"')
    #После обработки всех токенов в стеке должно остаться одно число
    if len(stack) != 1:
        raise IncorrectExpressionError('Введено неправильное RPN выражение')
    return stack[0]
