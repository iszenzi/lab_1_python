from calculator import tokenize, calculate
from constants import OPERATIONS
from exceptions import *

def main() -> float | int:
    """
    Читает RPN выражение, написанное пользователем, вычисляет результат выражения
    :return: результат RPN выражения
    """
    rpn_string = str(input('Введите RPN выражение:'))
    tokens = tokenize(string=rpn_string)
    result = calculate(string=rpn_string)
    return result


    
if __name__ == "__main__":
    print('Результат =', main())