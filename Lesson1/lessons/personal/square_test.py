from square import Square

"""This is exclusively for demonstrational purposes"""

class SquareTest():
    """For testing"""

    @staticmethod
    def test_positives():
        """For testing"""
        nums = {1: 1, 2: 4, 3: 9, 12: 144, 4: 16, 15: 225}

        for key, val in nums.items():
            res = Square.calc(key)

            if res != val:
                msg = f"""The calculation for {key} using your library was {res}. 
                This does not match {val}. Please retry/look into re-writing library."""
                print(msg)

    @staticmethod
    def test_negatives():
        """For testing"""
        nums = {-1: 1, -2: 4, -3: 9, -12: 144, -4: 16, -15: 225}

        for key, val in nums.items():
            res = Square.calc(key)

            if res != val:
                msg = f"""The calculation for {key} using your library was {res}. 
                This does not match {val}. Please retry/look into re-writing library."""
                print(msg)


if __name__ == "__main__":
    SquareTest.test_positives()
    SquareTest.test_negatives()
