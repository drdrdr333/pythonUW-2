""" Subtract class for providing the subtraction operation to Calculater """


class Subtract():
    @staticmethod
    def operate(a,b):
        """ Mathematical operation of subtract(a,b)
        Keyword arguments:
            a -> int
            b -> int
        Purpose:
            provide subtract functionality to Calculator
        Return: 
            a-b; ex. 6-5 -> 1
        """
        res = a-b
        return res