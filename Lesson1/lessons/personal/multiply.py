""" Multiply class for providing the multiply operation to Calculater """


class Multiply():
    @staticmethod
    def operate(a,b):
        """ Mathematical operation of multiply(a,b)
        Keyword arguments:
            a -> int
            b -> int
        Purpose:
            provide multiply functionality to Calculator
        Return: 
            a*b; ex. 5*5 -> 25
        """
        res = a*b
        return res