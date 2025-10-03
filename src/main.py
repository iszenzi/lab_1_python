from calculator import tokenize, calculate, CalcError
from constant import OPERATIONS

def main() -> float | int:
    """
    Читает RPN выражение, написанное пользователем, вычисляет результат выражения
    ::                                      # return ничего не выводит, поэтому использую print что указывать в :: тогда
    """
    rpn_string = str(input('Введите RPN выражение:'))
    try:
        tokens = tokenize(string=rpn_string)
        result = calculate(tokens=tokens)
        return result
    except:
        raise CalcError('Непредвиденная ошибка')
    
if __name__ == "__main__":
    print(main())



"""                 ВОПРОСЫ

нужен ли у функции main try except, если все ошибки обрабатываются в calculator.py? Добавить внутрь калькулятора и токенайзера все ошибки
программа должна работать то тех пор, пока пользователь не захочет или вчисляет только 1 выражение? пока не захочет

как обрабатывать скобки, если в RPN они ни на что не влияют, в выражении уже раставлены приоритеты? выкидвать скобки скобки запрещенный символ
# return ничего не выводит, поэтому использую print что указывать в :: тогда
"""
