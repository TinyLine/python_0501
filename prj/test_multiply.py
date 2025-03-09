import pytest

# def multiply_by_seven(numbers):
#     return [n * 7 for n in numbers]

# # Тест для порожнього списку
# def test_empty_list():
#     assert multiply_by_seven([]) == []

# # Тест для списку з одним елементом
# def test_single_element():
#     assert multiply_by_seven([3]) == [21]
#     assert multiply_by_seven([-1]) == [-7]

# # Тест для списку з кількох елементів
# def test_multiple_elements():
#     assert multiply_by_seven([1, 2, 3]) == [7, 14, 21]
#     assert multiply_by_seven([-1, -2, -3]) == [-7, -14, -21]

# # Тест для списку з великими числами
# def test_large_numbers():
#     assert multiply_by_seven([1000, 2000]) == [7000, 14000]

# # Тест для списку з нулями
# def test_zeros():
#     assert multiply_by_seven([0, 0, 0]) == [0, 0, 0]
    
    
    
    
    
def a(imp):
    imp = imp.upper()
    return imp
    
    
def is_palindrome(s):
   
    s = s.replace(" ", "")
    
    return s == s[::-1]


def test_a():
    assert a('hello') == 'HELLO'

def test_is_palindrome():
    assert is_palindrome('шалаш') == True
    
    
def test_integration():
    result = a('шалаш')  
    assert is_palindrome(result) == True  