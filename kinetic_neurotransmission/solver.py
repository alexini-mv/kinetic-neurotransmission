import math
import time
import warnings
from random import random

import pandas as pd 

class Solver:
    """ Define el solucionador encargado de realizar la evolución temporal del 
    kinetic neuromuscular transmission modelo, utilizando el algoritmo 
    estocástico de Gillespie (1976).

    Methods
    -------
    resting_state(time_end=30.0)
        Simular el modelo hasta alcanzar su resting state.
    run()
        Ejecuta el algoritmo de simulación para evolucionar temporalmente al 
        modelo. En este caso, sólo está implementado el algoritmo estocastico 
        de Gillespie. Los resultados se guardan en un pandas.DataFrame object.
    get_results()
        Regresa un pandas.DataFrame object con el resultado de la simulación del 
        modelo.
    get_resting_simulation()
        Regresa un pandas.DataFrame object con el resultado de la simulación del 
        modelo de la busqueda del resting state.
    """
    def __init__(self, model, stimulation):
        """ Inicializamos el objeto Solver, con el Model object previamente 
        definido y Stimulation object.

        Parameters
        ----------
        model: Model object
            Modelo que se simulará con el algoritmo de Gillespie. Este modelo 
            debe incluir todos los TransitionState, Transition y RateConstant 
            objects.
        stimulation: Stimulation object
            Objeto Stimulation que contiene la información del protocolo de 
            estimulación.
        """
        self.__model = model
        self.__stimulation = stimulation
        self.__resting_state = False

    def resting_state(self, time_end=30.0):
        """ Simula el modelo desde su estado inicial hasta alcanzar el 
        resting state.

        Parameters
        ----------
        time_end: float, optional
            Tiempo que evolucionara el modelo para alcanzar el resting state. 
            El tiempo se miden en segundos.
        """
        self.__gillespie(repeat=1, time_end=time_end, time_save=0.1, init_basal_state=True)
        self.__model.set_resting_state()
        self.__resting_state = True

    def run(self, repeat=1, time_end=1.0, time_save=0.0001, method='gillespie'):
        """ Metodo encargado de ejecutar al algoritmo encargado de evolucionar
        en el tiempo al modelo. Por default, se invoca al algoritmo estocastico
        de Gillespie.

        Parameters
        ----------
        repeat: int, optional
            Número de repeticiones que se simulara el modelo.
        time_end: float, optional
            Tiempo (segundos) en el cual finalizará la simulación del modelo.
        time_save: float, optional
            Intervalo de segundos en el cual se guardará periodicamente el 
            registro el estado instantaneo del modelo.
        method: str, optional
            Nombre del algoritmo que evolucionará temporalmente al modelo. 
            Actualmente sólo acepta 'gillespie'.
        """

        if not self.__resting_state: 
            message = "You have not set the resting state of the " + \
            "model. All simulations will start in a different state " + \
            "than the resting state."
            warnings.warn(message, Warning, stacklevel=2)

        if method == 'gillespie':
            self.__gillespie(repeat=repeat, time_end=time_end, time_save=time_save)
        else:
            message = f"Undefined method in '{self.__class__.__name__}'. " + \
            "The currently defined method is 'gillespie'."
            raise Exception(message)

    def __save_results(self, results: list, init_basal_state: bool):
        """ Guarda la evolución temporal del modelo en un pandas.DataFrame object.

        Parameters
        ----------
        results: list
            Lista donde se guarda temporalmente los resultados de la simulación.
        init_basal_state: bool
            Si el valor es 'True', indica que la simulación es para obtener el 
            resting state del modelo. En caso contrario, la simulación se ejecutará
            con normalidad.
        """
        if init_basal_state:
            self.__resting_state_simulation = pd.DataFrame(results).set_index(['run', 'time'])
        else:
            self.__results = pd.DataFrame(results).set_index(['run', 'time'])

    def get_results(self, mean: bool=False):
        """ Regresa el pandas.DataFrame object donde están guardados los 
        resultados de la simulación.

        Parameters
        ----------
        mean: bool
            Si el valor es 'True', regresará el promedio de la evolución temporal 
            de todas las repeticiones. En caso contrario, regresará la evolución 
            temporal de cada una de la repeticiones.

        Return
        ------
        pandas.DataFrame object
        """
        if mean:
            return self.__results.mean(level=1)
        else:       
            return self.__results

    def get_resting_simulation(self):
        """ Regresa un pandas.DataFrame object con el registro de la evolución 
        temporal del modelo durante la busqueda del resting state.
        """
        return self.__resting_state_simulation.mean(level=1)


    def __gillespie(self, repeat, time_end, time_save, init_basal_state=False):
        """ Metodo privado con la Implementación del Algoritmo Estocástico de 
        Gillespie (1976).

        Parameters
        ----------
        repeat: int
            Número de repeticiones que simulará el modelo.
        time_end: float
            Tiempo (en segundos) en el que finalizará la evolucion del modelo.
        time_save: float
            Intervalo de segundos en el cual se guardará periodicamente el 
            registro el estado instantaneo del modelo.
        init_basal_state: bool, optional
            Si el valor es 'true', se simulará el modelo para encontra su resting
            state. En caso contrario, se simulará la evolución del modelo
            considerando el protocolo de estimulación.
        """
        results = []
        for i in range(repeat):
            # -----------------------------------------------------------------
            # Initialize the model in its resting state previamente hallado.
            # -----------------------------------------------------------------
            self.__model.set_initial_state(self.__model.get_resting_state())

            t = 0.0
            tsave = 0.0

            # -----------------------------------------------------------------
            # Inicia el Algoritmo Estocastico de Gillespie
            # -----------------------------------------------------------------
            while True:
                a = {}
                #--------------------------------------------------------------
                # Se calculan los valores de propensión para cada transition
                #--------------------------------------------------------------
                for name, item in self.__model.get_transitions().items():
                    storage = list(item.get_origin().keys())[0]
                    dummy_vesicles = self.__model.get_transition_states()[storage].get_vesicles()
                    
                    if item.get_rate_constant().get_calcium_dependent() and not init_basal_state:
                        #------------------------------------------------------
                        # Se incluye la contribución de la estimulación
                        #------------------------------------------------------
                        dummy_rate = item.get_rate_constant().get_rate() + self.__stimulation.stimuli(t)
                    else:
                        dummy_rate = item.get_rate_constant().get_rate()

                    a.update({name: dummy_rate * dummy_vesicles})
                #--------------------------------------------------------------
                # Se calcula la propensión total del sistema
                #--------------------------------------------------------------
                a0 = sum(a.values())
                #--------------------------------------------------------------
                # Se calcula el tiempo en el que sucederá la siguiente transition
                #--------------------------------------------------------------
                t = t + math.log(1.0 / random()) / a0
                
                while t >= tsave:
                    #----------------------------------------------------------
                    # Guardamos el registro del estado instantaneo del modelo 
                    # dentro de una lista temporal.
                    #----------------------------------------------------------
                    dummy = {"run":i, "time": round(tsave, 9)}
                    dummy.update(self.__model.get_current_state())
                    results.append(dummy)
                    
                    tsave += time_save

                #--------------------------------------------------------------
                # Se elige aleatoreamente la siguiente transición que se 
                # ejecutará en dentro del modelo, considerando la propension
                # total del sistema.
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
                # Se obtienen los información del Transition objetc elegida.
                #--------------------------------------------------------------
                transition = self.__model.get_transitions()[transition_name]
                origin, vesicles_origin = list(transition.get_origin().items())[0]
                destination, vesicles_destination = list(transition.get_destination().items())[0]

                #--------------------------------------------------------------
                # Se ejecuta la transition actualizando el número de vesiculas 
                # en los TransitionState implicados en la Transition.
                #--------------------------------------------------------------
                self.__model.get_transition_states()[origin].pop_vesicle(vesicles_origin)
                self.__model.get_transition_states()[destination].add_vesicle(vesicles_destination)

                #--------------------------------------------------------------
                # Se repite el algoritmo hasta alcanzar tiempo final de la 
                # simulación.
                #--------------------------------------------------------------
                if tsave >= time_end:
                    break

        #----------------------------------------------------------------------
        # Se guardan los resultados de todas las repeticiones del algoritmo.
        #----------------------------------------------------------------------
        self.__save_results(results, init_basal_state)
