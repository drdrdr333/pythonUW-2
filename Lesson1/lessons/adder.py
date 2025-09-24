'''
    Adder module for our Calculator - performs a mathematical add operation
'''


class Adder:
    ''' Mathematical Adder '''
    @staticmethod
    def calc(operand_1, operand_2):
        """
            Mathematical add operation
        Keyword arguments:
            operand_1 -> int()
                first integer to be added, function will also convert
                to ensure it is of type int
            operand_2 -> int()
                second integer to be added, function will also
                convert to ensure it is of type int
        Return:
            operand_1+operand_2 = res -> 1+2=3; returns 3
        """
        res = int(operand_1) + int(operand_2)
        return res
