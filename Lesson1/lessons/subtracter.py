'''
    Subtract class for our Calculator -
    Performs the mathematical subtract operation
'''


class Subtracter:
    ''' mathematical subtract '''
    @staticmethod
    def calc(op_1, op_2):
        """
            Performs op_1 - op_2 in mathematical subtraction; ex. 3-2 -> 1
        Keyword arguments:
            op_1 -> int()
                first integer to be subtracted; will
                ensure type conversion to int()
            op_2 -> int()
                second integer to be subtracted; will
                ensure type conversion to int()
        Return:
            op_1 - op_2 -> res; 4-2=2; returns 2
        """
        res = int(op_1) - int(op_2)
        return res
