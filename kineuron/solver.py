import math
from random import random

import pandas as pd

from .kinetic_model import KineticModel
from .stimulation import Stimulation


class Solver:
    """It defines the solver in charge of performing the time evolution of the
    neuromuscular kinetic transmission model, using the Gillespie Stochastic 
    Algorithm (1977).

    Methods
    -------
    run
        Run the simulation algorithm to temporally evolve the model. The
        results are stored in a pandas.DataFrame object.
    resting_state
        Simulates the model until the resting state is reached.
    get_resting_simulation
        Returns a pandas.DataFrame object with the result of the simulation
        of the resting state search.
    get_results
        Returns a pandas.DataFrame object with the result of the model 
        simulation.
    """

    def __init__(self, model: KineticModel, stimulation: Stimulation) -> None:
        """Initializes the Solver object, with the previously defined Model
        object and Stimulation object.

        Parameters
        ----------
        model: kineuron.KineticModel object
            Model to be simulated. This model must include all 
            kineuron.TransitionState, kineuron.Transition and 
            kineuron.RateConstant objects.
        stimulation: kineuron.Stimulation object
            kineuron.Stimulation object containing the stimulation protocol 
            information.
        """
        self.__model: KineticModel = model
        self.__stimulation: Stimulation = stimulation
        self.__resting_state: bool = False

    def resting_state(self, time_end: float = 30.0) -> None:
        """Simulates the model from its initial state to the resting state.

        Parameters
        ----------
        time_end: float, optional
            Time that the model will evolve to reach the resting state. The time
            is measured in seconds.
        """
        self.__gillespie(repeat=1, time_end=time_end,
                         time_save=0.1, init_resting_state=True)
        self.__model.set_resting_state()
        self.__resting_state = True

    def run(self, repeat: int = 1, time_end: float = 1.0,
            time_save: float = 0.0001, method: str = 'gillespie') -> None:
        """Runs the time evolution algorithm of the model. By default, the
        Gillespie stochastic algorithm is invoked.

        Parameters
        ----------
        repeat: int, optional
            Number of repetitions that the model will be simulated.
        time_end: float, optional
            Time (seconds) at which the model simulation will finish.
        time_save: float, optional
            Interval of seconds in which the instantaneous state of the model
            will be saved periodically.
        method: str, optional
            Name of the algorithm to be used. Currently only accepts 'gillespie'.
        """

        msg = "You have not set the resting state of the model."
        assert self.__resting_state, msg

        if method == 'gillespie':
            self.__gillespie(repeat=repeat, time_end=time_end,
                             time_save=time_save)
        else:
            message = f"Undefined method in '{self.__class__.__name__}' " + \
                "object. The currently defined method is 'gillespie'."
            raise ValueError(message)

    def __save_results(self, results: list, init_resting_state: bool) -> None:
        """Saves the temporal evolution of the model in a pandas.DataFrame
        object.

        Parameters
        ----------
        results: list
            List that temporarily saves the results of the simulation.
        init_resting_state: bool
            If the value is 'True', it indicates that the simulation is to
            obtain the resting state of the model. Otherwise, the results are 
            from a common run.
        """
        if init_resting_state:
            self.__resting_state_simulation = pd.DataFrame(
                results).set_index(['run', 'time'])
        else:
            self.__results = pd.DataFrame(results).set_index(['run', 'time'])

    def get_results(self, mean: bool = False) -> pd.DataFrame:
        """Returns a pandas.DataFrame object containing the simulation results.

        Parameters
        ----------
        mean: bool
            If the value is 'True', it returns the average of the temporal
            evolution of all the repetitions. Otherwise, it returns the raw data.

        Return
        ------
        pandas.DataFrame object.
        """
        if mean:
            return self.__results.mean(level=1)
        else:
            return self.__results

    def get_resting_simulation(self) -> pd.DataFrame:
        """Returns the pandas.DataFrame object with the record of the time
        evolution during the resting state search.

        Return
        ------
        pandas.DataFrame object.
        """
        return self.__resting_state_simulation.mean(level=1)

    def __gillespie(self, repeat: int, time_end: float,
                    time_save: float, init_resting_state=False) -> None:
        """Implementation of Gillespie Stochastic Algorithm (1977).

        Parameters
        ----------
        repeat: int
            Number of repetitions to be simulated by the model.
        time_end: float
            Time (in seconds) at the end of the model evolution.
        time_save: float
            Interval of seconds in which the instantaneous state of the model
             is saved periodically.
        init_resting_state: bool, optional
            If the value is 'True', simulate the model to find its resting
            state. Otherwise, it simulates the evolution of the model
            considering the stimulation protocol.
        """
        results = []
        for i in range(repeat):
            # -----------------------------------------------------------------
            # Initialize the model in its previously found resting state.
            # -----------------------------------------------------------------
            self.__model.set_initial_state(self.__model.get_resting_state())

            t = 0.0
            tsave = 0.0

            # -----------------------------------------------------------------
            # Starts the Gillespie Stochastic Algorithm loop.
            # -----------------------------------------------------------------
            while True:
                a = {}

                # --------------------------------------------------------------
                # Propensity values are computed for each transition.
                # --------------------------------------------------------------
                for name, item in self.__model.get_transitions().items():
                    storage = item.get_origin()

                    dummy_vesicles = self.__model.get_transition_states()[
                        storage].get_vesicles()

                    dummy_rate = item.get_rate_constant().get_rate()

                    # ---------------------------------------------------------
                    # The contribution of Stimulation is included.
                    # ---------------------------------------------------------
                    if item.get_rate_constant().get_calcium_dependent() and not init_resting_state:
                        dummy_rate += self.__stimulation.stimuli(t)

                    # ---------------------------------------------------------
                    # Propensity value for each individual transition is saved
                    # ---------------------------------------------------------
                    a.update({name: dummy_rate * dummy_vesicles})

                # --------------------------------------------------------------
                # The total propensity of the system is calculated.
                # --------------------------------------------------------------
                a0 = sum(a.values())

                # --------------------------------------------------------------
                # The time in which the next transition will occur is calculated.
                # --------------------------------------------------------------
                t = t + math.log(1.0 / random()) / a0

                # -------------------------------------------------------------
                # The record of the instantaneous state of the model is stored
                # in a temporary list.
                # -------------------------------------------------------------
                while t >= tsave and tsave <= time_end:
                    dummy = {"run": i, "time": round(tsave, 9)}
                    dummy.update(self.__model.get_current_state())
                    results.append(dummy)

                    tsave += time_save

                # --------------------------------------------------------------
                # The next transition to be executed within the model is chosen
                # randomly, considering the total propensity of the system.
                # --------------------------------------------------------------
                random_a0 = random() * a0
                accumulative = 0.0

                for key, value in a.items():
                    transition_name = key
                    accumulative += value

                    if accumulative > random_a0:
                        break

                # --------------------------------------------------------------
                # The parameters defined in the selected kineuron.Transition
                # object are obtained.
                # --------------------------------------------------------------
                transition = self.__model.get_transitions()[transition_name]
                origin = transition.get_origin()
                destination = transition.get_destination()

                # --------------------------------------------------------------
                # The transition is executed by updating the number of vesicles
                # in the kineuron.TransitionState objects involved.
                # --------------------------------------------------------------
                self.__model.get_transition_states()[origin].pop_vesicle()
                self.__model.get_transition_states()[destination].add_vesicle()

                # --------------------------------------------------------------
                # The previous steps are repeated until the end time of the
                # simulation is reached.
                # --------------------------------------------------------------
                if tsave > time_end:
                    break

        # ----------------------------------------------------------------------
        # The results of all iterations of the algorithm are saved.
        # ----------------------------------------------------------------------
        self.__save_results(results, init_resting_state)
