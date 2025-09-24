'''
    Divider class for our Calculator -
    Performs mathematical divide operation
'''


class Divider:
    ''' Mathematical Divide '''
    @staticmethod
    def calc(op_1, op_2):
        """
            Performs mathematical divide on
            op_1/op_2; 4/2 -> 2
            exception for dividing by zero;
            4/0 -> exception
        Keyword arguments:
            op_1 -> int()
                first operand for division;
                ensures type is int()
            op_2 -> int()
                second operand for division;
                ensures type is int()
        Return:
            if op_2=0 -> ZeroDivisionError
            else
                op_1//op_2 -> res;
                ex. 10//5 -> 2 = res; return res
        """
        try:
            return op_1//op_2
        except Exception as e:
            raise ZeroDivisionError from e
