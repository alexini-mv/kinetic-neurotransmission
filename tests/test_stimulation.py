import unittest
from unittest.mock import patch

import numpy as np
from kineuron import Stimulation


class TestStimulation(unittest.TestCase):
    def setUp(self) -> None:
        self.parameters = {
            "conditional_stimuli": 3,
            "period": 0.1,
            "time_start_stimulation": 0.1,
            "tau_stimulus": 0.05,
            "time_wait_test": 0.15,
            "intensity_stimulus": 100.0,
            "type_stimulus": 'exponential_decay',
            "name": "Protocol"
        }
        self.stimulation = Stimulation(**self.parameters)

    def test_get_name(self) -> None:
        self.assertEqual(self.stimulation.get_name(), "Protocol")

    def test_type_stimulus_assert(self) -> None:
        self.parameters["type_stimulus"] = "linear_decay"

        with self.assertRaises(AssertionError):
            Stimulation(**self.parameters)

    def test_stimuli(self):
        actual = np.array([100.0,
                           41.111229050718734,
                           16.901331540606613,
                           51.34171190325921,
                           21.107208779109023,
                           64.11803884299545,
                           26.359713811572654,
                           10.836802322189591,
                           89.48393168143701,
                           36.787944117144285]
                          )
        t = np.linspace(0.1, 0.5, 10)
        desired = np.vectorize(self.stimulation.stimuli)(t)

        np.testing.assert_almost_equal(actual, desired)

    @patch("kineuron.stimulation.plt.show")
    def test_plot(self, mock_show):
        t = np.linspace(0.1, 0.5, 10)
        mock_show.assert_called()
        # Falta terminarlo


if __name__ == '__main__':
    unittest.main()
