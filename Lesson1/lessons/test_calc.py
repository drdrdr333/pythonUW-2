from adder import Adder
from subtracter import Subtracter
from multiplier import Multiplier
from divider import Divider
from calc import Calculator
from exceptions import InsufficientOperands
import unittest
from mock import Mock, MagicMock

'''
    Test file for calculator; includes both unit tests and integration tests
'''


class TestAdder(unittest.TestCase):
    def test_add_pos(self):
        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(Adder.calc(i, j), i+j)

    ##### extra tests using Mock #####
    # def test_add_positive(self):
    #     Adder.calc = Mock(return_value=3)
    #     expected = Adder.calc(1, 2)
    #     self.assertEqual(Adder.calc(), expected)

    # def test_add_negative(self):
    #     Adder.calc = Mock(return_value=-2)
    #     expected = Adder.calc(5, -7)
    #     self.assertEqual(Adder.calc(), expected)


class TestSubtracter(unittest.TestCase):
    def test_subtract(self):
        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(Subtracter.calc(i, j), i-j)

    ##### extra tests using Mock #####
    # def test_subtract_positive(self):
    #     Subtracter.calc = Mock(return_value=2)
    #     expected = Subtracter.calc(7, 5)
    #     self.assertEqual(Subtracter.calc(), expected)
    
    # def test_subtract_negative(self):
    #     Subtracter.calc = Mock(return_value=0)
    #     expected = Subtracter.calc(-3, -3)
    #     self.assertEqual(Subtracter.calc(), expected)


class TestMultiplier(unittest.TestCase):
    def test_multiplier(self):
        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(Multiplier.calc(i, j), i*j)

    ##### extra tests using Mock #####
    # def test_multiply_positive(self):
    #     Multiplier.calc = Mock(return_value=4)
    #     expected = Multiplier.calc(2,2)
    #     self.assertEqual(Multiplier.calc(), expected)

    #     _expected = Multiplier.calc(-2,-2)
    #     self.assertEqual(Multiplier.calc(), _expected)
    
    # def test_multiply_negative(self):
    #     Multiplier.calc = Mock(return_value=-4)
    #     expected = Multiplier.calc(2,-2)
    #     self.assertEqual(Multiplier.calc(), expected)

    #     _expected = Multiplier.calc(-2,2)
    #     self.assertEqual(Multiplier.calc(), _expected)

    
class TestDivider(unittest.TestCase):
    def test_divider(self):
        with self.assertRaises(ZeroDivisionError):
            for i in range(-10, 10):
                for j in range(-10, 10):
                    self.assertEqual(Divider.calc(i, j), i//j)

    ##### extra tests using Mock #####
    # def test_division(self):
    #     Divider.calc = Mock(return_value=2)
    #     expected = Divider.calc(4, 2)
    #     self.assertEqual(Divider.calc(), expected)


class TestCalculator(unittest.TestCase):
    def test_config(self):
        calc = Calculator(Adder, Subtracter, Multiplier, Divider)
        self.assertEqual(calc.adder, Adder)
        self.assertEqual(calc.subtracter, Subtracter)
        self.assertEqual(calc.multiplier, Multiplier)
        self.assertEqual(calc.divider, Divider)

    def test_enter_number(self):
        calc = Calculator(Adder, Subtracter, Multiplier, Divider)
        with self.assertRaises(ValueError):
            calc.enter_number('4 4 4')
        with self.assertRaises(NameError):
            calc.enter_number(four)
        calc.enter_number(1)
        self.assertEqual(calc.stack, [1])
        calc.enter_number(2)
        self.assertEqual(calc.stack, [1, 2])
        ex = calc.enter_number(3)
        self.assertEqual("You have typed 2 numbers. Please perform an operation!", ex)
    
    def test_stack_add(self):
        calc = Calculator(Adder, Subtracter, Multiplier, Divider)
        calc.enter_number(2)
        calc.enter_number(2)
        calc.add()
        self.assertEqual(calc.stack, [4])
    
    def test_stack_sub(self):
        calc = Calculator(Adder, Subtracter, Multiplier, Divider)
        calc.enter_number(2)
        calc.enter_number(2)
        calc.subtract()
        self.assertEqual(calc.stack, [0])
    
    def test_stack_mult(self):
        calc = Calculator(Adder, Subtracter, Multiplier, Divider)
        calc.enter_number(2)
        calc.enter_number(2)
        calc.multiply()
        self.assertEqual(calc.stack, [4])
    
    def test_stack_div(self):
        calc = Calculator(Adder, Subtracter, Multiplier, Divider)
        calc.enter_number(2)
        calc.enter_number(2)
        calc.divide()
        self.assertEqual(calc.stack, [1])

    #start of integrations
    def setUp(self):
        self.add = Adder()
        self.sub = Subtracter()
        self.multiply = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(self.add, self.sub, self.multiply, self.divider)

    def test_insufficient_operands(self):
        with self.assertRaises(InsufficientOperands):
            self.calculator.enter_number(0)
            self.calculator.add()

    def test_add_call(self):
        self.add.calc = MagicMock(return_value=0)
        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()
        self.add.calc.assert_called_with(1, 2)

    def test_add_call(self):
        self.sub.calc = MagicMock(return_value=0)
        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.subtract()
        self.sub.calc.assert_called_with(1, 2)

    def test_add_call(self):
        self.multiply.calc = MagicMock(return_value=0)
        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.multiply()
        self.multiply.calc.assert_called_with(1, 2)

    def test_add_call(self):
        self.divider.calc = MagicMock(return_value=0)
        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.divide()
        self.divider.calc.assert_called_with(1, 2)