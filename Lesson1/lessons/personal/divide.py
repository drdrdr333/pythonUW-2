""" Division class for providing the divide operation to Calculater """


class Divide():
    @staticmethod
    def operate(a,b):
        """ Mathematical operation of divide(a,b)
        Keyword arguments:
            a -> int
            b -> int
        Purpose:
            provide division functionality to Calculator
        Return: 
            a//b; ex. 25//5 -> 5
        """
        if a == 0 or b == 0:
            raise ZeroDivisionError("Unable to divide a number by 0, please try again!!")
        else:
            res = a//b
            return res