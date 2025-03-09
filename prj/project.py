import os
from work import log_message

def log_input(log_file):
    
    print("Введіть текст для запису в лог:")
    
    user_input = input(">>> ")
    
    if not user_input:
        print("Помилка: Порожній ввід не дозволений.")
        return False
    
    log_message(user_input, log_file)
    
    print("Повідомлення успішно записано в лог.")
    
    return True


def calc(log_file):
    
    print("Введіть операнди та операцію :")
    user_input1 = input("Перше число >>> ")
    user_input2 = input("Друге число >>> ")
    operation = input("Операція ")

    try:
        num1 = float(user_input1)
        num2 = float(user_input2)

        if operation == "+":
            result = num1 + num2
            
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        elif operation == "/":
            
            if num2 == 0:
                raise ZeroDivisionError("Ділення на нуль неможливе.")
            result = num1 / num2
        else:
            print("Помилка: Невідома операція.")
            return False

        print(f"Результат: {result}")
        log_message(f"Калькулятор: {num1} {operation} {num2} = {result}", log_file)
        
        print("Результат успішно записано в лог.")
        
        return True
    except ValueError:
        print("Помилка: Невірний ввід числа.")
        
        return False
    except ZeroDivisionError as e:
        
        print(f"Помилка: {e}")
        return False


def main():
    log_file = "log.txt"

    if not os.path.exists(log_file):
        print(f"Створення файлу: {log_file}")
        
        with open(log_file, "w") as f:
            
            f.write("=== Лог програми ===\n")


    while True:
        
        print("\nОберіть опцію:")
        print("1. Записати повідомлення в лог")
        print("2. Використати калькулятор")
        print("3. Вихід")
        
        choice = input(">>> ")

        if choice == "1":
            log_input(log_file)
        elif choice == "2":
            calc(log_file)
        elif choice == "3":
            print("Програма завершена.")
            break
        
        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()