from src.calculator import tokenize, calculate

def main() -> float | int:
    """
    Читает RPN выражение, написанное пользователем, вычисляет результат выражения
    :return: результат RPN выражения
    """
    rpn_string = str(input('Введите RPN выражение:'))
    tokens = tokenize(string=rpn_string)
    result = calculate(tokens=tokens)
    return result



if __name__ == "__main__":
    print('Результат =', main())

"""
исправить унарность брать первый символ, убирать его и запоминать, обрабатываем part без этого символа, если все норм, то в конце добавить унарный символ в токен, иначе ошибка неправильного токена
"""
