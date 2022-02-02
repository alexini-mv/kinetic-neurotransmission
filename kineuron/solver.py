import math
import warnings
from random import random

import pandas as pd 

class Solver:
    """It defines the solver in charge of performing the time evolution of the 
    neuromuscular kinetic transmission model, using the stochastic algorithm 
    of Gillespie (1976).

    Methods
    -------
    run()
        Run the simulation algorithm to temporally evolve the model. The 
        results are stored in a pandas.DataFrame object.
    resting_state(time_end=30.0)
        Simulates the model until the resting state is reached.
    get_resting_simulation()
        Returns a pandas.DataFrame object with the result of the simulation 
        of the resting state search.
    get_results()
        Returns a pandas.DataFrame object with the result of the model 
        simulation.
    """
    def __init__(self, model, stimulation):
        """Initializes the Solver object, with the previously defined Model 
        object and Stimulation object.

        Parameters
        ----------
        model: KineticModel object
            Model to be simulated. This model must include all TransitionState, 
            Transition and RateConstant objects.
        stimulation: Stimulation object
            Stimulation object containing the stimulation protocol information.
        """
        self.__model = model
        self.__stimulation = stimulation
        self.__resting_state = False

    def resting_state(self, time_end=30.0):
        """Simulates the model from its initial state to the resting state.

        Parameters
        ----------
        time_end: float, optional
            Time that the model will evolve to reach the resting state. The time 
            is measured in seconds.
        """
        self.__gillespie(repeat=1, time_end=time_end, time_save=0.1, init_basal_state=True)
        self.__model.set_resting_state()
        self.__resting_state = True

    def run(self, repeat=1, time_end=1.0, time_save=0.0001, method='gillespie'):
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

        if not self.__resting_state: 
            message = "You have not set the resting state of the " + \
            "model. All simulations will start in a different state " + \
            "than the resting state."
            warnings.warn(message, Warning, stacklevel=2)

        if method == 'gillespie':
            self.__gillespie(repeat=repeat, time_end=time_end, time_save=time_save)
        else:
            message = f"Undefined algorithm in '{self.__class__.__name__}'. " + \
            "The currently defined algorithm is 'gillespie'."
            raise Exception(message)

    def __save_results(self, results: list, init_basal_state: bool):
        """Saves the temporal evolution of the model in a pandas.DataFrame 
        object.

        Parameters
        ----------
        results: list
            List that temporarily saves the results of the simulation.
        init_basal_state: bool
            If the value is 'True', it indicates that the simulation is to 
            obtain the resting state of the model. Otherwise, the simulation 
            will run normally.
        """
        if init_basal_state:
            self.__resting_state_simulation = pd.DataFrame(results).set_index(['run', 'time'])
        else:
            self.__results = pd.DataFrame(results).set_index(['run', 'time'])

    def get_results(self, mean: bool=False):
        """Returns the pandas.DataFrame object containing the simulation results.

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

    def get_resting_simulation(self):
        """Returns the pandas.DataFrame object with the record of the time 
        evolution during the resting state search.

        Return
        ------
        pandas.DataFrame object.
        """
        return self.__resting_state_simulation.mean(level=1)


    def __gillespie(self, repeat, time_end, time_save, init_basal_state=False):
        """Implementation of Gillespie's Stochastic Algorithm (1976).

        Parameters
        ----------
        repeat: int
            Number of repetitions to be simulated by the model.
        time_end: float
            Time (in seconds) at the end of the model evolution.
        time_save: float
            Interval of seconds in which the instantaneous state of the model 
            will be saved periodically.
        init_basal_state: bool, optional
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
                #--------------------------------------------------------------
                # Propensity values are computed for each transition.
                #--------------------------------------------------------------
                for name, item in self.__model.get_transitions().items():
                    storage = list(item.get_origin().keys())[0]
                    dummy_vesicles = self.__model.get_transition_states()[storage].get_vesicles()
                    
                    if item.get_rate_constant().get_calcium_dependent() and not init_basal_state:
                        #------------------------------------------------------
                        # The contribution of stimulation is included.
                        #------------------------------------------------------
                        dummy_rate = item.get_rate_constant().get_rate() + self.__stimulation.stimuli(t)
                    else:
                        dummy_rate = item.get_rate_constant().get_rate()

                    a.update({name: dummy_rate * dummy_vesicles})
                #--------------------------------------------------------------
                # The total propensity of the system is calculated.
                #--------------------------------------------------------------
                a0 = sum(a.values())
                #--------------------------------------------------------------
                # The time in which the next transition will occur is calculated.
                #--------------------------------------------------------------
                t = t + math.log(1.0 / random()) / a0
                
                while t >= tsave:
                    #----------------------------------------------------------
                    # The record of the instantaneous state of the model is 
                    # stored in a temporary list.
                    #----------------------------------------------------------
                    dummy = {"run":i, "time": round(tsave, 9)}
                    dummy.update(self.__model.get_current_state())
                    results.append(dummy)
                    
                    tsave += time_save

                #--------------------------------------------------------------
                # The next transition to be executed within the model is chosen 
                # randomly, considering the total propensity of the system.
                #--------------------------------------------------------------
                random_a0 = random() * a0
                accumulative = 0.0

                for key, value in a.items():
                    transition_name = key
                    accumulative += value

                    if accumulative < random_a0:
                        continue
                    else:
                        break
                
                #--------------------------------------------------------------
                # The parameters defined in the selected Transition object are 
                # obtained.
                #--------------------------------------------------------------
                transition = self.__model.get_transitions()[transition_name]
                origin, vesicles_origin = list(transition.get_origin().items())[0]
                destination, vesicles_destination = list(transition.get_destination().items())[0]

                #--------------------------------------------------------------
                # The transition is executed by updating the number of vesicles 
                # in the TransitionState objects involved.
                #--------------------------------------------------------------
                self.__model.get_transition_states()[origin].pop_vesicle(vesicles_origin)
                self.__model.get_transition_states()[destination].add_vesicle(vesicles_destination)

                #--------------------------------------------------------------
                # The previous steps are repeated until the end time of the 
                # simulation is reached.
                #--------------------------------------------------------------
                if tsave >= time_end:
                    break

        #----------------------------------------------------------------------
        # The results of all iterations of the algorithm are saved.
        #----------------------------------------------------------------------
        self.__save_results(results, init_basal_state)
