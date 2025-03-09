import unittest

def sum_and_difference(a, b):
    return a + b, a - b, a / b, a * b


result = sum_and_difference(10, 5)
print("Сума:", result[0])
print("Різниця:", result[1])
print("Ділення:", result[2])
print("Добуток:", result[3])

if __name__ == "__main__":
    unittest.main()
    
    
 