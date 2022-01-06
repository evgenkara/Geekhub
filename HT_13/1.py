"""
Створити клас Calc, який буде мати атребут last_result та 4 методи. Методи повинні виконувати математичні операції
з 2-ма числами, а саме додавання, віднімання, множення, ділення.
   - Якщо під час створення екземпляру класу звернутися до атребута last_result він повинен повернути пусте значення
   - Якщо використати один з методів - last_result повенен повернути результат виконання попереднього методу.
   - Додати документування в клас
"""


class Calc(object):
    """
    A class used to do some math calculations
    :param last_result: The result of previous calculation(None by default)
    :param result: The result of last calculation(None by default)
    """
    last_result = None
    result = None

    def add(self, x, y):
        """
        Adds 2 numbers
        """
        self.last_result = self.result
        self.result = x + y

    def subtract(self, x, y):
        """
        Subtracts x from y
        """
        self.last_result = self.result
        self.result = x - y

    def mult(self, x, y):
        """
        Multiplies 2 numbers
        """
        self.last_result = self.result
        self.result = x * y

    def divide(self, x, y):
        """
        Divides x by y
        """
        self.last_result = self.result
        if y != 0:
            self.result = x / y
        else:
            self.result = "Can't divide by 0"


c = Calc()
c.add(12, 3)
print(c.last_result)
c.divide(12, 0)
print(c.last_result)
c.divide(15, 3)
print(c.last_result)
