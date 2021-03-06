import os
import random
import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from kineuron import (KineticModel, RateConstant, Solver, Stimulation,
                      Transition, TransitionState)



class TestSolver(unittest.TestCase):
    def setUp(self) -> None:
        self.model = KineticModel(name='my-model', vesicles=100)

        docked = TransitionState(name='Docked')
        fusion = TransitionState(name='Fusion')
        self.list_transition_states = [docked, fusion]
        self.model.add_transition_states(self.list_transition_states)

        alpha = RateConstant(name="α", value=0.3, calcium_dependent=True)
        beta = RateConstant(name="β", value=15)

        tr1 = Transition(name='Transition 1',
                         rate_constant=alpha,
                         origin="Docked",
                         destination="Fusion"
                         )
        tr2 = Transition(name='Transition 2',
                         rate_constant=beta,
                         origin="Fusion",
                         destination="Docked"
                         )
        self.list_transitions = [tr1, tr2]
        self.model.add_transitions(self.list_transitions)
        self.model.init()

        parameters = {"conditional_stimuli": 5,
                      "period": 0.03,
                      "time_start_stimulation": 0.1,
                      "tau_stimulus": 0.0013,
                      "time_wait_test": 0.2,
                      "intensity_stimulus": 1000.0,
                      "type_stimulus": "exponential_decay",
                      "name": "Custom Stimulation Protocol"
                      }
        self.protocol = Stimulation(**parameters)

        self.experiment = Solver(model=self.model, stimulation=self.protocol)

    def test_not_init_model(self) -> None:
        model2 = KineticModel(name='my-model-2', vesicles=100)
        model2.add_transition_states(self.list_transition_states)
        model2.add_transitions(self.list_transitions)
        experiment = Solver(model=model2, stimulation=self.protocol)

        self.assertRaises(AssertionError, experiment.resting_state)

    def test_not_resting_state(self) -> None:
        self.assertRaises(AssertionError, self.experiment.run)

    def test_resting_state(self) -> None:
        random.seed(135)
        self.experiment.resting_state()

        self.assertTrue(self.model._init_resting_state)

        self.assertIsInstance(
            self.experiment.get_resting_simulation(), pd.DataFrame)

        self.assertDictEqual(
            self.model.get_resting_state(), {'Docked': 98, 'Fusion': 2})

    def test_reset_init(self) -> None:
        random.seed(36)
        for _ in range(3):
            self.experiment.resting_state()

        vesicles = sum(self.model.get_current_state().values())

        self.assertEqual(vesicles, self.model.get_vesicles())

    def test_not_gillespie(self) -> None:
        self.experiment.resting_state()
        self.assertRaises(ValueError, self.experiment.run, method="custom")

    def test_run(self) -> None:
        random.seed(46)
        file = os.path.join(os.getcwd(),
                            "tests",
                            "__statics",
                            "test_run_results.csv")

        actual_run_results = pd.read_csv(file, index_col="time")
        self.experiment.resting_state()
        self.experiment.run(repeat=10, time_end=1.0, time_save=0.0005,
                            save_transitions=["Transition 1", "Transition 2"])

        self.assertIsInstance(self.experiment.get_results(), pd.DataFrame)

        assert_frame_equal(
            self.experiment.get_results(mean=True), actual_run_results)

    def test_number_vesicles_final(self) -> None:
        self.experiment.resting_state()
        self.experiment.run(repeat=1, time_end=120.0, time_save=1.0)
        vesicles = sum(self.model.get_current_state().values())

        self.assertEqual(vesicles, self.model.get_vesicles())

    def test_save_transitions(self) -> None:
        self.experiment.resting_state()

        self.assertRaises(ValueError, self.experiment.run,
                          save_transitions=["Custom Transition"])

        self.experiment.run(save_transitions=["Transition 1", "Transition 2"])
        results = self.experiment.get_results(mean=False)
        transition_set = {"Transition 1", "Transition 2"}

        self.assertTrue(transition_set.issubset(set(results.columns)))


if __name__ == '__main__':
    unittest.main()
