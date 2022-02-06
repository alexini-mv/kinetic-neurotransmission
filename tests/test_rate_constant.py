import unittest
from kineuron import RateConstant

class TestRateConstant(unittest.TestCase):

    def test_get_name(self):
        rate = RateConstant("alpha", value=1.5)
        self.assertEqual(rate.get_name(), "alpha")

    def test_get_rate(self):
        rate = RateConstant("alpha", value=1.5)
        self.assertEqual(rate.get_rate(), 1.5)

    def test_calcium_dependence(self):
        rate = RateConstant("alpha", value=1.5, calcium_dependent=True)
        self.assertEqual(rate.get_calcium_dependent(), True)