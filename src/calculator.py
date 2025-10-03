from src.constant import OPERATIONS


class CalcError(Exception):
    pass


def tokenize(string: str) -> list[(str, float | int | None)]:                       # не знаю как правильно записать ->
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
    parts = str(string).replace('(','').replace(')','').split()                      #мб и не нужно обрабатывать скобки
    if not parts:
        raise CalcError('Пустая строка')
    operations = OPERATIONS
    for part in parts:                                           # пока что есть ошибки с *********** 2**2 и тп(но если написать else:raise то нет ошибок)
        try:
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
                                                                                        ### ДОБАВИТЬ ТОКЕН E0F - А надо ли?
            else:
                raise CalcError(f'Неизвестный токен "{part}"')
        except:
            raise CalcError(f'Незивестный токен "{part}"')
    return tokens


def calculate(tokens: list[(str, float | int | None)]) -> float | int:
    """
    Вычисляет значение RPN выражения
    :param string: RPN выражение, записанное пользователем
    :return: Возвращает результат вычисления RPN выражения 
    """
    stack = []
    operations = OPERATIONS
    for token_type, token_value in tokens:
        #Добавление числа в стек
        if token_type == 'NUMBER':
            stack.append(token_value)
        #Проверка возможности выполнения операции
        elif token_type in operations:
            if len(stack) < 2:
                raise CalcError(f'Недостаточно чисел для оператора "{token_type}"')
            b = stack.pop() #второе число
            a = stack.pop() #первое число
            #Проверка деления на 0
            if token_type in ['/', '//', '%'] and b == 0:
                raise CalcError('Деление на ноль')
            #Для операторов // и % числа должны быть целыми
            if token_type in ['//', '%']:
                if (a % 1 == 0) + (b % 1 == 0) != 2:
                    raise CalcError(f'Для операции "{token_type}" нужны целые числа')
                else:
                    stack.append(operations[token_type](a, b))
            if token_type in ['+', '-', '*', '**']:
                stack.append(operations[token_type](a, b))
        else:
            raise CalcError(f'Неизвестный токен "{token_type}"')
    #После обработки всех токенов в стеке должно остаться одно число
    if len(stack) != 1:
        raise CalcError('Неправильное RPN выражение')
    return stack[0]

