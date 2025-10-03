from src.constant import OPERATIONS
from src.exceptions import *

def tokenize(string: str) -> list[(str, float | int | None)]: 
    """
    Разбивает строку на токены: числа и операторы
    Кладет полученные токены в список
    Для целого числа кладем в список ('NUMBER', int())
    Для вещественного числа кладем в список ('NUMBER', float())
    Для оператора кладем в список ('Оператор', None)
    :param string: RPN выражение, записанное пользователем
    :return: Возвращает список токенов
    """
    tokens = []
    parts = str(string).split() 
    if not parts:
        raise EmptyStringError('Введена пустая строка')
    operations = OPERATIONS
    for part in parts:                                         
        #Добавление токена вещественного числа
        if part.count('.') == 1:
            part_float = part.split('.')
            """
            lstrip удалит все + или - слева, если + или - будет один,т.е. число является унарным, 
            то оно сможет преобразоваться во float()/int(), но если знаков будет > чем 1,
            то except выведет ошибку, так как float()/int() не преобразует число --5
            """
            if ''.join(part_float).lstrip('+-').isdigit():
                tokens.append(('NUMBER', float(part)))
        #Добавление токена целого числа
        elif part.lstrip('+-').isdigit():
            
            tokens.append(('NUMBER', int(part)))
        #Добавление токена оператора 
        elif part in operations:
            tokens.append((f'{part}', None))
        else:
            raise UnknownTokenError(f'Неизвестный токен "{part}"')
    return tokens


def calculate(string: str) -> float | int:
    """
    Вычисляет значение RPN выражения
    :param string: RPN выражение, записанное пользователем
    :return: Возвращает результат вычисления RPN выражения 
    """
    stack = []
    tokens = tokenize(string)
    operations = OPERATIONS
    for token_type, token_value in tokens:
        #Добавление числа в стек
        if token_type == 'NUMBER':
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

