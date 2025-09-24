'''
    Multiplier class for our Calculator -
    Performs mathematical multiply operation
'''


class Multiplier:
    ''' Mathematical Multiply '''
    @staticmethod
    def calc(op_1, op_2):
        """
            Multiplies op_1 and op_2; ex 2*2 -> 4
        Keyword arguments:
            op_1 -> int()
                first operand to multiply; ensures it is of int() type
            op_2 -> int()
                second operand to multiply; ensures it is of int() type
        Return:
            op_1*op_2 -> res; return res; 2*2=4, return 4
        """
        res = op_1*op_2
        return res
