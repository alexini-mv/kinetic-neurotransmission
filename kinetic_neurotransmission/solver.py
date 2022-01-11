import math
import time
import warnings
from random import random

import pandas as pd 

class Solver:
    """ Se define el solucionador encargado de realizar la evolución del modelo
    utilizando el algoritmo estocastico de Gillespie.

    Methods
    -------
    resting_state
        Metodo encargado de simular el modelo hasta alcanzar su estado de reposo.
    run
        Metodo encargado de correr el algoritmo de simulación. En este caso, está
        implementado el algoritmo de Gillespie. Pero desde aquí se podría invocar
        cualquier otro algoritmo de solución que se desee implementar.

    save_results
        Metodo privado que guarda el resultado de la simulación del modelo en 
        un DataFrame de Pandas dentro del objeto.
    get_results
        Regresa un DataFrame de Pandas con el resultado de la simulación del 
        modelo.
    get_resting_simulation
        Regresa un DataFrame de Pandas con el resultado de la simulación del 
        modelo cuando se busca el estado estacionario.
    gillespie
        Metodo privado en donde se establece el algoritmo de Gillespie.
    """
    def __init__(self, model, stimulation):
        """ Inicializamos el objeto Solver, con el modelo previamente definido y
        el protocolo de estimulación

        Parameters
        ----------
        synapse: Model object
            Modelo que se simulará. Este modelo debe incluir los estados 
            cinéticos, los objetos reacciones, los objetos velocidades de reacción.
        stimulation: Stimulation object
            Objeto definico que contiene la información del protocolo de 
            estimulación externa a lo largo del tiempo.
        """
        self.__model = model
        self.__stimulation = stimulation
        self.__resting_state = False

    def resting_state(self, time_end=30.0):
        """ Simula el modelo en su estado inicial y lo lleva al estado 
        estacionario o de reposo. Para esto, utiliza el algoritmo de Gillespie
        para evolucionar en el tiempo al modelo.

        Parameters
        ----------
        time_end: float, optional
            Tiempo que evolucionara el modelo para alcanzar el estado 
            estacionario. La unidad de tiempo se miden en segundos.
        """
        self.__gillespie(repeat=1, time_end=time_end, time_save=0.1, init_basal_state=True)
        self.__model.set_resting_state()
        self.__resting_state = True

    def run(self, repeat=1, time_end=1.0, time_save=0.0001, method='gillespie'):
        """ Metodo encargado de invocar al algoritmo encargado de evolucionar
        en el tiempo al modelo. Por default, se invocará al algoritmo de gillespie,
        pero en caso de definir otro algoritmo, aquí se debe invocar.

        Parameters
        ----------
        repeat: int, optional
            Número de repeticiones se simulara el modelo.
        time_end: float, optional
            Tiempo (segundos) en el que finalizara la evolución temporal del modelo.
        time_save: float, optional
            Intervalo de segundos que guardará reiterativamente en un registro 
            el estado instantaneo del modelo.
        method: str, optional
            Nombre del algoritmo que evolucionará temporalmente al modelo. 
            Actualmente sólo acepta 'gillespie'.
        """

        if not self.__resting_state: 
            message = "You have not set the resting state of the \
                model. All simulations will start in a different state \
                than the resting state."
            warnings.warn(message, Warning, stacklevel=2)

        if method == 'gillespie':
            self.__gillespie(repeat=repeat, time_end=time_end, time_save=time_save)
        else:
            message = f"Undefined method in '{self.__class__.__name__}'. \
                The currently defined method is 'gillespie'."
            raise Exception(message)

    def __save_results(self, results: list, init_basal_state: bool):
        """ Guarda la evolución temporal del modelo en un DataFrame de Pandas.

        Parameters
        ----------
        results: list
            Lista donde se guarda temporalmente los resultados de la simulación.
        init_basal_state: bool
            Si el valor es 'true', indica que la simulación es para obtener el 
            estado estacionario del modelo y guardará los resultados en el atributo
            privado stationary_state_simulation. En caso contrario, guardará los
            resultados en el atributo privado results.
        """
        if init_basal_state:
            self.__resting_state_simulation = pd.DataFrame(results).set_index(['run', 'time'])
        else:
            self.__results = pd.DataFrame(results).set_index(['run', 'time'])

    def get_results(self, mean: bool=False):
        """ Regresa los resultados de la simulación en un DataFrame de Panda.

        Parameters
        ----------
        mean: bool
            Si el valor es 'true', regresará la evolución temporal promedio del 
            modelo, promediado sobre el número total de repeticiones. En caso 
            contrario, regresará la evolución temporal de cada una de 
            la repeticiones.

        Return
        ------
        Return a Pandas.DataFrame Object.
        """
        if mean:
            return self.__results.mean(level=1)
        else:       
            return self.__results

    def get_resting_simulation(self):
        """ Regresa el DataFrame de Pandas con la evolución temporal del modelo
        durante la busqueda del estado estacionario del mismo.
        """
        return self.__resting_state_simulation.mean(level=1)


    def __gillespie(self, repeat, time_end, time_save, init_basal_state=False):
        """ Metodo privado con la Implementación del Algoritmo Estocástico de 
        Gillespie.

        Parameters
        ----------
        repeat: int
            Número de repeticiones que simulará el modelo.
        time_end: float
            Tiempo en segundo en el que finalizará la evolucion del modelo.
        time_save: float
            Cada cuanto tiempo se guardará el registro del estado instantaneo 
            del modelo.
        init_basal_state: bool, optional
            Si el valor es 'true', se simulará el modelo para encontra su estado
            estacionario. En caso contrario, se simulará la evolución del modelo
            considerando el protocolo de estimulación externa.
        """
        results = []
        for i in range(repeat):
            # Initialize the synapse in its stationary state previamente hallado.
            self.__model.set_initial_state(self.__model.get_resting_state())

            t = 0.0
            tsave = 0.0

            while True:
                a = {}
                #--------------------------------------------------------------
                # Se calculan los valores de propensión para cada reacción
                #--------------------------------------------------------------
                for name, item in self.__model.get_transitions().items():
                    storage = list(item.get_origin().keys())[0]
                    dummy_vesicles = self.__model.get_transition_states()[storage].get_vesicles()
                    
                    if item.get_rate_constant().get_calcium_dependent() and not init_basal_state:
                        #------------------------------------------------------
                        # Aquí se incluye la contribución de la estimulación
                        # externa
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
                # Se calcula el tiempo en el que sucederá la siguiente reacción
                #--------------------------------------------------------------
                t = t + math.log(1.0 / random()) / a0
                
                while t >= tsave:
                    #----------------------------------------------------------
                    # Guardamos el registro del estado instantaneo del modelo 
                    # en una lista temporal.
                    #----------------------------------------------------------
                    dummy = {"run":i, "time": round(tsave, 9)}
                    dummy.update(self.__model.get_current_state())
                    results.append(dummy)

                    tsave += time_save

                #--------------------------------------------------------------
                # Se elige aleatoreamente la siguiente transición que se 
                # ejecutará en dentro del modelo
                #--------------------------------------------------------------
                r2a0 = random() * a0
                accumulative = 0.0

                for key, value in a.items():
                    transition_name = key
                    accumulative += value

                    if accumulative < r2a0:
                        continue
                    else:
                        break
                
                #--------------------------------------------------------------
                # Se obtienen los información guardada del objeto de la 
                # reacción elegida.
                #--------------------------------------------------------------
                transition = self.__model.get_transitions()[transition_name]

                origin, vesicles_origin = list(transition.get_origin().items())[0]
                destination, vesicles_destination = list(transition.get_destination().items())[0]

                #--------------------------------------------------------------
                # Se actualiza el número de vesiculas en los estados cinéticos 
                # implicados en la reacción elegida.
                #--------------------------------------------------------------
                self.__model.get_transition_states()[origin].pop_vesicle(vesicles_origin)
                self.__model.get_transition_states()[destination].add_vesicle(vesicles_destination)

                #--------------------------------------------------------------
                # Se repite el algoritmo hasta alcanzar tiempo final de la 
                # simulación
                #--------------------------------------------------------------
                if tsave >= time_end:
                    break

        #----------------------------------------------------------------------
        # Se guardan los resultados de todas las repeticiones del algoritmo.
        #----------------------------------------------------------------------
        self.__save_results(results, init_basal_state)
