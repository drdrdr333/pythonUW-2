""" Add class for providing the add operation to Calculater """


class Add():
    @staticmethod
    def operate(a,b):
        """ Mathematical operation of add(a,b)
        Keyword arguments:
            a -> int
            b -> int
        Purpose:
            provide add functionality to Calculator
        Return: 
            a+b; ex. 5+5 -> 10
        """
        res = a+b
        return res