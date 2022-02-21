import os
import random
import unittest
from unittest.mock import patch

import pandas as pd
import numpy as np
from kineuron import (KineticModel, RateConstant, Solver, Stimulation,
                      Transition, TransitionState)
from pandas.testing import assert_frame_equal


class TestSolver(unittest.TestCase):
    def setUp(self) -> None:
        model = KineticModel(name='my-model', vesicles=100)

        docked = TransitionState(name='Docked')
        fusion = TransitionState(name='Fusion')
        model.add_transition_states([docked, fusion])

        alpha = RateConstant(name="α", value=0.3, calcium_dependent=True)
        beta = RateConstant(name="β", value=15)
        model.add_rate_constants([alpha, beta])

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
        model.add_transitions([tr1, tr2])
        model.init()

        parameters = {"conditional_stimuli": 5,
                      "period": 0.03,
                      "time_start_stimulation": 0.1,
                      "tau_stimulus": 0.0013,
                      "time_wait_test": 0.2,
                      "intensity_stimulus": 1000.0,
                      "type_stimulus": "exponential_decay",
                      "name": "Custom Stimulation Protocol"
                      }
        protocol = Stimulation(**parameters)

        self.experiment = Solver(model=model, stimulation=protocol)

    def test_not_resting_state(self) -> None:
        self.assertRaises(AssertionError, self.experiment.run)

    def test_resting_state(self) -> None:
        random.seed(135)
        file = os.path.join(os.getcwd(),
                            "tests",
                            "__statics",
                            "test_resting_state.csv")
        actual_resting_state = pd.read_csv(file, index_col="time")
        self.experiment.resting_state()

        self.assertIsInstance(
            self.experiment.get_resting_simulation(), pd.DataFrame)
        assert_frame_equal(
            self.experiment.get_resting_simulation(), actual_resting_state)

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
        self.experiment.run(repeat=10, time_end=1.0, time_save=0.0005)

        self.assertIsInstance(self.experiment.get_results(), pd.DataFrame)
        assert_frame_equal(
            self.experiment.get_results(mean=True), actual_run_results)


if __name__ == '__main__':
    unittest.main()
