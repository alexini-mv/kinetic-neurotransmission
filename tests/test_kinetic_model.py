import unittest
from unittest.mock import patch

from kineuron import KineticModel, RateConstant, Transition, TransitionState


class TestKineticModel(unittest.TestCase):
    def setUp(self) -> None:
        self.model = KineticModel(name='my-model', vesicles=100)

        docked = TransitionState(name='Docked')
        fusion = TransitionState(name='Fusion')

        self.list_transition_states = [docked, fusion]
        self.model.add_transition_states(self.list_transition_states)

        alpha = RateConstant(name="α", value=0.3, calcium_dependent=True)
        beta = RateConstant(name="β", value=15)

        self.list_rate_constants = [alpha, beta]
        self.model.add_rate_constants(self.list_rate_constants)

        tr1 = Transition(name='Transition 1',
                         rate_constant=alpha,
                         origin={"Docked": 1},
                         destination={"Fusion": 1}
                         )
        tr2 = Transition(name='Transition 2',
                         rate_constant=beta,
                         origin={"Fusion": 1},
                         destination={"Docked": 1}
                         )
        self.list_transitions = [tr1, tr2]
        self.model.add_transitions(self.list_transitions)

    def test_get_name(self) -> None:
        self.assertEqual(self.model.get_name(), "my-model")

    def test_get_vesicles(self) -> None:
        self.assertEqual(self.model.get_vesicles(), 100)

    def test_get_transition_states(self) -> None:
        dict_transition_states = {item.get_name(): item
                                  for item in self.list_transition_states}

        self.assertDictEqual(
            self.model.get_transition_states(), dict_transition_states)

    def test_get_transitions(self) -> None:
        dict_transitions = {item.get_name(): item
                            for item in self.list_transitions}

        self.assertDictEqual(
            self.model.get_transitions(), dict_transitions)

    def test_get_current_state(self) -> None:
        dict_current_state = {item.get_name(): item.get_vesicles()
                              for item in self.list_transition_states}

        self.assertDictEqual(
            self.model.get_current_state(), dict_current_state)

    @patch("kineuron.kinetic_model.Digraph")
    def test_get_graph(self, mock_digraph) -> None:
        self.model.get_graph()

        mock_digraph.assert_called()


if __name__ == '__main__':
    unittest.main()
