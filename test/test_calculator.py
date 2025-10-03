import pytest
from src.calculator import calculate, tokenize, CalcError 




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
