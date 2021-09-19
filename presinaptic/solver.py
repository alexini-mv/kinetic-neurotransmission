import math
import time
import warnings
from random import random

import pandas as pd 

class Solver:
    def __init__(self, synapse, protocol):
        self.__synapse = synapse
        self.__protocol = protocol
        self.__stationary_state = False

    def stationary_state(self, time_end=30):
        self.__gillespie(repeat=1, time_end=time_end, time_save=0.1, init_basal_state=True)
        self.__synapse.set_stationary_state()
        self.__stationary_state = True

    def run(self, repeat=1, time_end=1.0, time_save=0.0001, method='gillespie'):
        if not self.__stationary_state: 
            message = "You have not set the stationary state of the synapse. All simulations will start in a different state than the stationary state."
            warnings.warn(message, Warning, stacklevel=2)

        if method == 'gillespie':
            self.__gillespie(repeat=repeat, time_end=time_end, time_save=time_save)
        else:
            message = f"Undefined method in '{self.__class__.__name__}'. The currently defined method is 'gillespie'."
            raise Exception(message)

    def __save_results(self, results: list, init_basal_state: bool):
        if init_basal_state:
            self.__stationary_state_simulation = pd.DataFrame(results).set_index(['run', 'time'])
        else:
            self.__results = pd.DataFrame(results).set_index(['run', 'time'])

    def get_results(self, mean: bool=False):
        if mean:
            return self.__results.mean(level=1)
        else:       
            return self.__results

    def get_stationary_simulation(self):
        return self.__stationary_state_simulation.mean(level=1)


    def __gillespie(self, repeat, time_end, time_save, init_basal_state=False):
        results = []
        for i in range(repeat):
            # Initialize the synapse in its stationary state
            self.__synapse.set_initial_state(self.__synapse.get_stationary_state())

            t = 0.0
            tsave = 0.0

            while True:
                a = {}
                for name, item in self.__synapse.get_reactions().items():
                    storage = list(item.get_origin().keys())[0]
                    dummy_vesicles = self.__synapse.get_kinetic_states()[storage].get_vesicles()
                    
                    if item.get_rate_reaction().get_stimulation() and not init_basal_state:
                        dummy_rate = item.get_rate_reaction().get_rate() + self.__protocol.stimuli(t)
                    else:
                        dummy_rate = item.get_rate_reaction().get_rate()

                    a.update({name: dummy_rate * dummy_vesicles})

                a0 = sum(a.values())

                t = t + math.log(1.0 / random()) / a0
                
                while t >= tsave:
                    # Versión donde guardamos todo en una lista y después lo guardamos en un DataFrame

                    dummy = {"run":i, "time": round(tsave, 9)}
                    dummy.update(self.__synapse.get_current_state())
                    results.append(dummy)

                    tsave += time_save

                r2a0 = random() * a0
                accumulative = 0.0

                for key, value in a.items():
                    reaction_name = key
                    accumulative += value

                    if accumulative < r2a0:
                        continue
                    else:
                        break
                
                reaction = self.__synapse.get_reactions()[reaction_name]

                origin, vesicles_origin = list(reaction.get_origin().items())[0]
                destination, vesicles_destination = list(reaction.get_destination().items())[0]

                self.__synapse.get_kinetic_states()[origin].pop_vesicle(vesicles_origin)
                self.__synapse.get_kinetic_states()[destination].add_vesicle(vesicles_destination)

                # ************** Falta agregar las condiciones cuando los estados se quedan sin vesiculas ******

                # *********************************************************************************************
                if tsave >= time_end:
                    break

        self.__save_results(results, init_basal_state)
