import pytest
from src.calculator import calculate, tokenize
from src.exceptions import *



def test_tokenize_float():
    assert tokenize('   12.435  ') == [('NUMBER', 12.435)]
    assert tokenize('1111111111.11111111111') == [('NUMBER', 1111111111.11111111111)]

def test_tokenize_int():
    assert tokenize('3      82   5') == [('NUMBER', 3), ('NUMBER', 82), ('NUMBER', 5)]

def test_tokenize_unary():
    assert tokenize('-3 +5  -22 +1') == [('NUMBER', -3), ('NUMBER', 5), ('NUMBER', -22), ('NUMBER', 1)]
    assert tokenize(' +3.14  -5.2 -13.3') == [('NUMBER', 3.14), ('NUMBER', -5.2), ('NUMBER', -13.3)]

def test_tokenize_operations():
    assert tokenize(' +  -  /   // %  *') == [('+', None), ('-', None), ('/', None), ('//', None), ('%', None), ('*', None)]

def test_tokenize_expression():
    assert tokenize(' 3 4 +') == [('NUMBER', 3), ('NUMBER', 4), ('+', None)]
    assert tokenize('2  5  * 2 +') == [('NUMBER', 2), ('NUMBER', 5), ('*', None), ('NUMBER', 2), ('+', None)]

def test_calculate_integer_operations():
    assert calculate('10 2 //') == 5
    assert calculate('-25  5  //') == -5
    assert calculate('19 3  %') == 1
    assert calculate('-21 4 %') == 3

def test_caluclate_non_integer_operations():
    assert calculate('13.2 16 +') == 29.2
    assert calculate('14.5 7 -') == 7.5
    assert calculate('7 3.1 *') == 21.7
    assert calculate('2 5 **') == 32
    assert calculate('5 -3 **') == 1 / 125

def test_tokenize_empty_srting_raises():
    with pytest.raises(EmptyStringError) as exc_info:
        tokenize('')
    assert 'Введена пустая строка' in str(exc_info.value)
    assert exc_info.type is EmptyStringError

def test_tokenize_unknown_token_raises():
    with pytest.raises(UnknownTokenError) as exc_info:
        tokenize(' :(  ')
    assert 'Неизвестный токен ":("' in str(exc_info.value)
    assert exc_info.type is UnknownTokenError

def test_calculate_integer_numbers_raises():
    with pytest.raises(IntegerNumbersError) as exc_info:
        calculate(' 10.2 2 //')
    assert 'Для операции "//" нужны целые числа' in str(exc_info.value)
    assert exc_info.type is IntegerNumbersError

def test_calculate_not_enough_numbers_raises():
    with pytest.raises(NotEnoughNumbersError) as exc_info:
        calculate(' 52 +')
    assert 'Недостаточно чисел для оператора "+"' in str(exc_info.value)
    assert exc_info.type is NotEnoughNumbersError

def test_calculate_incorrect_expression_raises():
    with pytest.raises(IncorrectExpressionError) as  exc_info:
        calculate('2 3 + 4 * 1')
    assert 'Введено неправильное RPN выражение' in str(exc_info.value)
    assert exc_info.type is IncorrectExpressionError