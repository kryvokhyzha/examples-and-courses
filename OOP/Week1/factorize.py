class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        for x in (1.5, 'string'):
            with self.subTest(x=x):
                self.assertRaises(TypeError, factorize, x)

    def test_negative(self):
        for x in (-1, -10, -100):
            with self.subTest(x=x):
                self.assertRaises(ValueError, factorize, x)

    def test_zero_and_one_cases(self):
        for x, answer in ((0, (0,)), (1, (1,))):
            with self.subTest(x=x):
                self.assertEqual(factorize(x), answer)

    def test_simple_numbers(self):
        for x in (3, 13, 29):
            with self.subTest(x=x):
                self.assertEqual(factorize(x), (x,))

    def test_two_simple_multipliers(self):
        for x, answer in ((6, (2, 3)), (26, (2, 13)), (121, (11, 11))):
            with self.subTest(x=x):
                self.assertEqual(factorize(x), answer)

    def test_many_multipliers(self):
        for x, answer in ((1001, (7, 11, 13)),
         (9699690, (2, 3, 5, 7, 11, 13, 17, 19))):
            with self.subTest(x=x):
                self.assertEqual(factorize(x), answer)
