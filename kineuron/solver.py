import math
from random import choice, random

import pandas as pd
from tqdm.auto import trange

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

    def __resting_test(self, dataframe: pd.DataFrame, window_width: int,
                       tolerance: float) -> tuple[dict, bool]:
        """Auxiliary function that evaluates whether the model simulation has 
        reached its resting state. The procedure of time averaging over moving 
        time windows is followed. If the variation of the averages is less 
        than the 'tolerance', then it is accepted that the resting state of 
        the model has been reached.

        Parameters
        ----------
        dataframe: pandas.DataFrame
            Dataframe with the complete simulation record.
        window_width: int
            Number of columns with which the time average is be made.
        tolerance: float
            Percentage variation of vesicles tolerated in the kinetic states 
            to accept the resting state.

        Return
        ------
        dict
            Dictionary with the name of the kinetic states and their numbers 
            of vesicles corresponding to the resting state.
        bool
            Flag indicating that the resting state was found.
        """
        df = dataframe.rolling(window_width).mean(
        ).iloc[range(0, len(dataframe), window_width)]
        df2 = abs(100.0 * df.diff() / float(self.__model.get_vesicles()))
        df2 = df2.dropna().sum(axis=1)

        try:
            index = df2[df2 < tolerance].idxmin()
            state = df.loc[index].round().astype('int').to_dict()

            difference = self.__model.get_vesicles() - sum(state.values())
            if difference != 0:
                random_name = choice(list(state.keys()))
                state[random_name] += difference

            return state, True

        except ValueError:
            return {}, False

    def resting_state(self, time_end: float = 300.0,
                      window_width: int = 3000,
                      tolerance: float = 0.5) -> None:
        """Simulates the model from its initial state to the resting state.

        Parameters
        ----------
        time_end: float, optional
            Time that the model will evolve to reach the resting state. The 
            time is measured in seconds.
        window_width: int, optional
            Number of columns with which the time averaging is done to find 
            the resting state.
        tolerance: float, optional
            Percentage variation of vesicles tolerated in the kinetic states 
            to accept the resting state.
        """
        message = "The model is not initialized. Make sure to include " + \
            "the 'KineticModel.init()' method."
        assert self.__model._init_flag, message

        print("\nDetermining Resting State...")

        for _ in trange(3, desc="Attempt",
                        ascii=True, colour="green", initial=1, leave=False,
                        bar_format="{desc}: {n_fmt}/{total_fmt} |{bar}|"):

            self.__gillespie(repeat=1, time_end=time_end, time_save=0.01,
                             resting_state_simulation=True)

            state, success = self.__resting_test(
                self.get_resting_simulation(), window_width, tolerance)

            if success:
                print("Set resting state...")
                self.__model.set_resting_state(state)
                print("Done")
                break

        if not success:
            msg = "The system has not reached its resting state with the " + \
                "specified 'tolerance'. Please, try to search with a " + \
                "higher 'tolerance'."
            print(msg)

    def run(self, repeat: int = 1, time_end: float = 1.0,
            time_save: float = 0.0001, method: str = 'gillespie',
            save_transitions: list = []) -> None:
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
        save_transitions: list, optional
            List with the name of the transitions that individual events will
            be included in the final results.
        """
        message = "The resting state has not been set in the model. Make sure " + \
            "to include the 'Solver.resting_state()' statement."
        assert self.__model._init_resting_state, message

        print("\nRunning Simulation of Model...")

        for element in save_transitions:
            if element not in self.__model.get_transitions().keys():
                message = f"'{element}' is not a defined name of any " + \
                    "kineuron.Transition object in Model."
                raise ValueError(message)

        if method == 'gillespie':
            self.__gillespie(repeat=repeat, time_end=time_end,
                             time_save=time_save,
                             save_transitions=save_transitions)
        else:
            message = f"Undefined method in '{self.__class__.__name__}' " + \
                "object. The currently defined method is 'gillespie'."
            raise ValueError(message)

    def __save_results(self, results: list,
                       resting_state_simulation: bool) -> None:
        """Saves the temporal evolution of the model in a pandas.DataFrame
        object.

        Parameters
        ----------
        results: list
            List that temporarily saves the results of the simulation.
        resting_state_simulation: bool
            If the value is 'True', it indicates that the simulation is to
            obtain the resting state of the model. Otherwise, the results are
            from a common run.
        """
        if resting_state_simulation:
            self.__resting_state_simulation = pd.DataFrame(
                results).set_index(['run', 'time']).droplevel(level=0)
        else:
            print("Generating results...")
            self.__results = pd.DataFrame(results).set_index(['run', 'time'])
            print("Done")

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
            return self.__results.groupby(level=1).mean()
        else:
            return self.__results

    def get_resting_simulation(self) -> pd.DataFrame:
        """Returns the pandas.DataFrame object with the record of the time
        evolution during the resting state search.

        Return
        ------
        pandas.DataFrame object.
        """
        return self.__resting_state_simulation

    def __list2dictzero(self, dummylist: list) -> dict:
        """Auxiliary function that converts a list of strings into a
        dictionary with the values initialized to zero.

        Parameters
        ----------
        dummylist: list
            List with strings elements.

        Return
        ------
        dict
            Dictionary with elements of list as keys and all values
            initialized to zero.
        """
        return {element: 0 for element in dummylist}

    def __gillespie(self, repeat: int, time_end: float, time_save: float,
                    resting_state_simulation: bool = False,
                    save_transitions: list = []) -> None:
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
        resting_state_simulation: bool, optional
            If the value is 'True' simulate the model to find its resting
            state. Otherwise, it simulates the evolution of the model
            considering the stimulation protocol.
        save_transitions: list, optional
            List with the name of the transitions that individual events will
            be included in the final results.
        """
        results = []

        for i in trange(repeat, desc="Progress: ", ascii=True, colour="green", disable=resting_state_simulation):
            # -----------------------------------------------------------------
            # Initialize the model in its previously found resting state.
            # -----------------------------------------------------------------
            self.__model.set_initial_state(self.__model.get_resting_state())

            t = 0.0
            tsave = 0.0
            dummy_transitions = self.__list2dictzero(save_transitions)

            # -----------------------------------------------------------------
            # Starts the Gillespie Stochastic Algorithm loop.
            # -----------------------------------------------------------------
            while tsave <= time_end:
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
                    if item.get_rate_constant().get_calcium_dependent() and \
                            not resting_state_simulation:

                        dummy_rate += self.__stimulation.stimuli(t)
                    # ---------------------------------------------------------
                    # Propensity value for each individual transition is saved
                    # ---------------------------------------------------------
                    a.update({name: dummy_rate * dummy_vesicles})

                # -------------------------------------------------------------
                # The total propensity of the system is calculated.
                # -------------------------------------------------------------
                a0 = sum(a.values())

                # -------------------------------------------------------------
                # The time in which the next transition will occur is calculated.
                # -------------------------------------------------------------
                t = t + math.log(1.0 / random()) / a0

                # -------------------------------------------------------------
                # The record of the instantaneous state of the model is stored
                # in a temporary list.
                # -------------------------------------------------------------
                while t >= tsave and tsave <= time_end:
                    dummy = {"run": i, "time": round(tsave, 9)}
                    dummy.update(self.__model.get_current_state())
                    dummy.update(dummy_transitions)

                    results.append(dummy)

                    dummy_transitions = self.__list2dictzero(save_transitions)
                    tsave += time_save

                # -------------------------------------------------------------
                # The next transition to be executed within the model is chosen
                # randomly, considering the total propensity of the system.
                # -------------------------------------------------------------
                random_a0 = random() * a0
                accumulative = 0.0

                for key, value in a.items():
                    transition_name = key
                    accumulative += value

                    if accumulative > random_a0:
                        break

                # -------------------------------------------------------------
                # The parameters defined in the selected kineuron.Transition
                # object are obtained.
                # -------------------------------------------------------------
                transition = self.__model.get_transitions()[transition_name]
                origin = transition.get_origin()
                destination = transition.get_destination()

                # -------------------------------------------------------------
                # The transition is executed by updating the number of vesicles
                # in the kineuron.TransitionState objects involved.
                # -------------------------------------------------------------
                self.__model.get_transition_states()[origin].pop_vesicle()
                self.__model.get_transition_states()[destination].add_vesicle()

                # -------------------------------------------------------------
                # The individual transition event is recorded for attachment to
                # the results.
                # -------------------------------------------------------------
                if transition_name in save_transitions:
                    dummy_transitions[transition_name] += 1

                # -------------------------------------------------------------
                # The previous steps are repeated until the end time of the
                # simulation is reached.
                # -------------------------------------------------------------
        # ---------------------------------------------------------------------
        # The results of all iterations of the algorithm are saved.
        # ---------------------------------------------------------------------
        self.__save_results(results, resting_state_simulation)
        del results
