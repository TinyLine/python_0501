class Animal:
    def __init__(self, name, eat):
        self.name = name
        self.eat = eat

    def allAnimals(self):
        print('Всі тварини люблять людей.')

    def food(self):
        print(f'{self.name} любить їсти {self.eat}.')
    
    def sound(self):
        print('*Тварини видають звуки*')


class Cat(Animal):
    def __init__(self, color, name, eat):  
        self.color = color
        self.name = name
        self.eat = eat
        self.__danger = 'Кіт може подряпати'

    def sleep(self):
        print(f'{self.color} кіт {self.name} любить поспати.')
        
    def sound(self):
        print(f'{self.name} каже: Мяу!')

    def get_danger(self):
        return self.__danger


    def set_danger(self, new_danger):
        self.__danger = new_danger


class Dog(Animal):
    def __init__(self, color, name, eat): 
        self.color = color
        self.name = name
        self.eat = eat
        self.__danger = 'Собака може вкусити'

    def sound(self):
        print(f'{self.name} каже: Гав!')

    def no_sleep(self):
        print(f'{self.color} пес {self.name} завжди дуже енергійний.')

    def get_danger(self):
        return self.__danger

    def set_danger(self, new_danger):
        self.__danger = new_danger






cat1 = Cat('Чорний', 'Василь', 'рибу')
dog1 = Dog('Коричневий', 'Петро', 'кістки')


cat1.food()          
cat1.sleep()
cat1.allAnimals()        
print(cat1.get_danger())  

dog1.food()          
dog1.no_sleep()
dog1.allAnimals()     
print(dog1.get_danger())  


animals = [cat1, dog1]

for animal in animals:
    animal.sound()
