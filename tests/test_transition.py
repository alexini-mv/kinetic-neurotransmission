import unittest

from kineuron import RateConstant, Transition


class TestTransition(unittest.TestCase):

    def setUp(self) -> None:
        rate_constant = RateConstant(name="alpha",
                                     value=1.5,
                                     calcium_dependent=True
                                     )
        self.transition = Transition(name="Transition 1",
                                     rate_constant=rate_constant,
                                     origin={"Docker": 1},
                                     destination={"Fusion": 1}
                                     )

    def test_get_name(self) -> None:
        self.assertEqual(self.transition.get_name(), "Transition 1")

    def test_get_rate_constant(self) -> None:
        self.assertIsInstance(
            self.transition.get_rate_constant(), RateConstant)

    def test_get_origin(self) -> None:
        self.assertDictEqual(self.transition.get_origin(), {"Docker": 1})

    def test_get_destination(self) -> None:
        self.assertDictEqual(self.transition.get_destination(), {"Fusion": 1})


if __name__ == '__main__':
    unittest.main()
