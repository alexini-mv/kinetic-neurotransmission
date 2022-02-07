import unittest
from kineuron import TransitionState

class TestTransitionState(unittest.TestCase):

    def setUp(self) -> None:
        self.transition_state = TransitionState(name="Docker")

    def test_get_name(self):
        self.assertEqual(self.transition_state.get_name(), "Docker")

    def test_inicial_vesicle(self):
        self.assertEqual(self.transition_state.get_vesicles(), 0)

    def test_update(self):
        self.transition_state.update(125)
        self.assertEqual(self.transition_state.get_vesicles(), 125)

    def test_add_vesicle(self):
        self.transition_state.update(35)
        self.transition_state.add_vesicle(1)
        self.assertEqual(self.transition_state.get_vesicles(), 36)

    def test_pop_vesicle(self):
        self.transition_state.update(35)
        self.transition_state.pop_vesicle(1)
        self.assertEqual(self.transition_state.get_vesicles(), 34)


if __name__ == '__main__':
    unittest.main()