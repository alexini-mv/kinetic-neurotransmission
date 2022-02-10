import unittest

from kineuron import RateConstant


class TestRateConstant(unittest.TestCase):

    def setUp(self) -> None:
        self.rate_constant = RateConstant(name="alpha",
                                          value=1.5,
                                          calcium_dependent=True
                                          )

    def test_get_name(self) -> None:
        self.assertEqual(self.rate_constant.get_name(), "alpha")

    def test_get_rate(self) -> None:
        self.assertEqual(self.rate_constant.get_rate(), 1.5)

    def test_calcium_dependence(self) -> None:
        self.assertTrue(self.rate_constant.get_calcium_dependent())

    def test_not_calcium_dependence(self) -> None:
        rate = RateConstant("alpha", value=1.0)
        self.assertFalse(rate.get_calcium_dependent())


if __name__ == '__main__':
    unittest.main()
