import pytest
from src.calculator import calculate, tokenize2
from src.exceptions import (
    UnknownTokenError,
    EmptyStringError,
    NotEnoughNumbersError,
    IncorrectExpressionError,
    IntegerNumbersError
)



def test_tokenize_float() -> None:
    assert tokenize2('   12.435  ') == [('NUMBER', 12.435)]
    assert tokenize2('1111111111.11111111111') == [('NUMBER', 1111111111.11111111111)]

def test_tokenize_int() -> None:
    assert tokenize2('3      82   5') == [('NUMBER', 3), ('NUMBER', 82), ('NUMBER', 5)]

def test_tokenize_unary() -> None:
    assert tokenize2('-3 +5  -22 +1') == [('NUMBER', -3), ('NUMBER', 5), ('NUMBER', -22), ('NUMBER', 1)]
    assert tokenize2(' +3.14  -5.2 -13.3') == [('NUMBER', 3.14), ('NUMBER', -5.2), ('NUMBER', -13.3)]

def test_tokenize_operations() -> None:
    assert tokenize2(' +  -  /   // %  *') == [('+', None), ('-', None), ('/', None), ('//', None), ('%', None), ('*', None)]

def test_tokenize_expression() -> None:
    assert tokenize2(' 3 4 +') == [('NUMBER', 3), ('NUMBER', 4), ('+', None)]
    assert tokenize2('2  5  * 2 +') == [('NUMBER', 2), ('NUMBER', 5), ('*', None), ('NUMBER', 2), ('+', None)]

def test_calculate_integer_operations() -> None:
    assert calculate([('NUMBER', 10), ('NUMBER', 2), ('//', None)]) == 5
    assert calculate([('NUMBER', -25), ('NUMBER', 5), ('//', None)]) == -5
    assert calculate([('NUMBER', 19), ('NUMBER', 3), ('%', None)]) == 1
    assert calculate([('NUMBER', -21), ('NUMBER', 4), ('%', None)]) == 3


def test_caluclate_non_integer_operations() -> None:
    assert calculate([('NUMBER', 13.2), ('NUMBER', 16), ('+', None)]) == 29.2
    assert calculate([('NUMBER', 14.5), ('NUMBER', 7), ('-', None)]) == 7.5
    assert calculate([('NUMBER', 7), ('NUMBER', 3.1), ('*', None)]) == 21.7
    assert calculate([('NUMBER', 2), ('NUMBER', 5), ('**', None)]) == 32
    assert calculate([('NUMBER', 5), ('NUMBER', -3), ('**', None)]) == 1 / 125

def test_tokenize_empty_srting_raises() -> None:
    with pytest.raises(EmptyStringError) as exc_info:
        tokenize2('')
    assert 'Введена пустая строка' in str(exc_info.value)
    assert exc_info.type is EmptyStringError

def test_tokenize_unknown_token_raises() -> None:
    with pytest.raises(UnknownTokenError) as exc_info:
        tokenize2(' :(  ')
    assert 'Неизвестный токен ":("' in str(exc_info.value)
    assert exc_info.type is UnknownTokenError

def test_calculate_integer_numbers_raises() -> None:
    with pytest.raises(IntegerNumbersError) as exc_info:
        calculate([('NUMBER', 10.2), ('NUMBER', 2), ('//', None)])
    assert 'Для операции "//" нужны целые числа' in str(exc_info.value)
    assert exc_info.type is IntegerNumbersError

def test_calculate_not_enough_numbers_raises() -> None:
    with pytest.raises(NotEnoughNumbersError) as exc_info:
        calculate([('NUMBER', 52), ('+', None)])
    assert 'Недостаточно чисел для оператора "+"' in str(exc_info.value)
    assert exc_info.type is NotEnoughNumbersError

def test_calculate_incorrect_expression_raises() -> None:
    with pytest.raises(IncorrectExpressionError) as  exc_info:
        calculate([('NUMBER', 2), ('NUMBER', 3), ('+', None), ('NUMBER', 4), ('*', None), ('NUMBER', 1)])
    assert 'Введено неправильное RPN выражение' in str(exc_info.value)
    assert exc_info.type is IncorrectExpressionError
