from src.calculator import calculate, tokenize2

def main() -> float | int:
    """
    Читает RPN выражение, написанное пользователем, вычисляет результат выражения
    :return: результат RPN выражения
    """
    rpn_string = str(input('Введите RPN выражение:'))
    tokens = tokenize2(string=rpn_string)
    result = calculate(tokens=tokens)
    return result

if __name__ == "__main__":
    print('Результат =', main())
