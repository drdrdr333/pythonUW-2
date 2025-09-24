""" Base Calculator
    
    Provides addition, multiplication,
    subtraction and division capabilities.
    
    Only accepts 2 numbers.
    Very basic."""


import divide, subtract, add, multiply


class Calculator():
    """ See above - this is implementation of Calculator abstraction """
    def __init__(self):
        """Constrctor
                -numbers - holds the two numbers we want to perform an operation upon"""
        self.numbers = []

    
    def enter_number(self, a):
        """Adds a number to a memory location to use for a math operation
        
        Keyword arguments:
            a -> int 
                a number to store
        
        Purpose:
            Store numbers in Calculator

        Return:
            None
        """
        
        if self.numbers.__len__() >= 2:
            self.numbers.clear()
            self.numbers.append(a)
        else:
            self.numbers.append(a)
    

    def add(self):
        if self.numbers.__len__() <= 1:
            raise Exception("Insufficient operands presented. Please enter another number.")
        try:
            res = add.Add.operate(self.numbers[0], self.numbers[1])
        except (ValueError, TypeError):
            print("Please retry your calculation...")
        finally:
            if res:
                print(f"{self.numbers[0]} + {self.numbers[1]} = {res}")
    

    def subtract(self):
        if self.numbers.__len__() <= 1:
            raise Exception("Insufficient operands presented. Please enter another number.")
        try:
            res = subtract.Subtract.operate(self.numbers[0], self.numbers[1])
        except (ValueError, TypeError):
            print("Please retry your calculation...")
        finally:
            if res:
                print(f"{self.numbers[0]} - {self.numbers[1]} = {res}")


    def multiply(self):
        if self.numbers.__len__() <= 1:
            raise Exception("Insufficient operands presented. Please enter another number.")
        try:
            res = multiply.Multiply.operate(self.numbers[0], self.numbers[1])
        except (ValueError, TypeError):
            print("Please retry your calculation...")
        finally:
            if res:
                print(f"{self.numbers[0]} * {self.numbers[1]} = {res}")
    

    def divide(self):
        if self.numbers.__len__() <= 1:
            raise Exception("Insufficient operands presented. Please enter another number.")
        try:
            res = divide.Divide.operate(self.numbers[0], self.numbers[1])
        except (ValueError, TypeError):
            print("Please retry your calculation...")
        finally:
            if res:
                print(f"{self.numbers[0]} / {self.numbers[1]} = {res}")