"""
    Fully functional calculator
    Performs +, -, /, *
    on a set of 2 numbers
"""

from exceptiongroup import ExceptionGroup
from exceptions import InsufficientOperands


class Calculator:
    ''' Calculator for performing four basic
        math operation
    '''
    def __init__(self, _add, _sub, _mult, _div):
        self.adder = _add
        self.subtracter = _sub
        self.multiplier = _mult
        self.divider = _div
        self.stack = []

    def enter_number(self, num):
        """
            Allows us to enter a number
            in the calculator
            1 number per call
        Keyword arguments:
            num -> int()
                the number to place into
                the stack, the first operand used
                in our operation
        Return:
            None - if an integer is not entered
            raises a TypeError, ValueError
        """
        try:
            if len(self.stack) == 2:
                msg = "You have typed 2 numbers. Please perform an operation!"
                return msg
            num_int = int(num)
            self.stack.append(num_int)
            return None
        except ExceptionGroup as exc:
            raise ExceptionGroup([ValueError, NameError]) from exc

    def _do_calc(self, operation):
        """ Performs the math operation
            that it is supplied with
        Keyword arguments:
            operation -> object();
            either: Adder, Subtracter, Multiplier,
            Divider
                the operation we want to perform
        Return:
            if self.stack has less than 2 numbers
            returns InsufficientOperands
            else perform the operation and the operation
            returns a result
        """
        try:
            res = operation.calc(self.stack[0], self.stack[1])
            return res
        except IndexError as i:
            raise InsufficientOperands from i

    def add(self):
        ''' Leverages _do_calc & adder to perform operation '''
        res = self._do_calc(self.adder)
        self.stack = [res]
        return res

    def subtract(self):
        ''' Leverages _do_calc & subtracter to perform operation '''
        res = self._do_calc(self.subtracter)
        self.stack = [res]
        return res

    def multiply(self):
        ''' Leverages _do_calc & multiplier to perform operation '''
        res = self._do_calc(self.multiplier)
        self.stack = [res]
        return res

    def divide(self):
        ''' Leverages _do_calc & divider to perform operation '''
        res = self._do_calc(self.divider)
        self.stack = [res]
        return res
