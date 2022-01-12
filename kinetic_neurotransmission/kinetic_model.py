from graphviz import Digraph
from .neuromuscular import Synapse

class KineticModel(Synapse):
    """Define el modelo cinético para modelar las fases de 
    maduración de las vesículas en la terminal sináptica nerviosa.

    Attributs
    ---------
    vesicles : int
        Número de vesiculas totales que se simularán en el modelo cinético.
    transition_states : dict
        Diccionario con el nombre y valores de los objetos TransitionState del modelo.
    transitions : dict
        Diccionario con el nombre y valores de los objetos Transition del modelo.
    rates : dict
        Diccionario con el nombre y valores de los objetos RateConstant de transición 
        entre los TransitionState vesiculares del modelo.

    Methods
    -------
    add_rate_constants(rates : list)
        Agrega al modelo la lista de todos los objetos RateConstant de cada
        transición cinética vesicular.
    add_transition_states(transition_states : list)
        Agrega al modelo la lista de todos los objetos TransitionState que componen
        al modelo.
    add_transitions(transitions : list)
        Agrega al modelo la lista de todas las Transition entre los TransitionState 
        del modelo.
    get_vesicle
        Imprime el numero total de vesiculas que se están simulando en el modelo.
    get_transition_states
        Regresa una lista con todos los TransitionState definidos en el 
        modelo.
    get_transitions
        Regresa una lista con todos las Transition entre estados cinéticos 
        definidos en el modelo.
    get_current_state
        Regresa un diccionario con el nombre y número de vesículas instantaneo en 
        cada uno de los estados cinéticos definidos en el modelo.
    get_info
        Regresa varios strings con la información general del modelo, es decir, 
        el nombre de las estados cinéticos vesiculares, reacciones entre estados
        cinéticos, velocidades de reacción, número de vesiculas simuladas.
    init
        Inicializa el modelo con los objetos agregados y prepararlo para comenzar 
        la simulación.
    set_initial_state(dictionary_state : dict)
        Se establece un estado inicial del modelo (nombre y número de vesiculas
        en cada estado cinetico vesicular) a partir del cual se simulará el modelo.
    set_resting_state
        Define el resting state del modelo del modelo.
    get_resting_state
        Regresa un diccionario con el nombre y el número de vesiculas en cada
        estado cinético vesicular correspondiente al resting state del modelo.
    get_graph
        Regresa un gráfo con la información de modelo, es decir, el nombre de 
        los estados cinéticos vesiculares, transitions y rate constants.
    """

    def __init__(self, name, vesicles=10000):
        """ Inicializamos el modelo cinético para simular las transiciones
        entre los diferentes estados vesiculares.

        Parameters
        ----------
        name : str
            Nombre del modelo.
        vesicles : int, optional
            Número total de vesiculas que serán simuladas en el modelo.
        """
        super().__init__(name)
        self.__vesicles = vesicles

    def __dict_items(self, list_items):
        """ Función auxiliar para convertir una lista de items a un diccionario.
        
        Parameters
        ----------
        list_items : list
            Lista de items que será convertido en diccionario.

        Return
        ------
        dict
            Diccionario con el nombre de cada item como key, y el objeto como 
            valor.
        """
        return {item.get_name(): item for item in list_items}

    def add_rate_constants(self, rates=[]):
        """ Agrega objetos tipo RateConstant dentro del modelo.

        Parameters
        ----------
        rates : list
            Lista de objetos tipo RateConstant.
        """
        self.__rates = self.__dict_items(rates)

    def add_transition_states(self, transition_states=[]):
        """ Agrega objetos tipo TransitionState dentro del modelo.

        Parameters
        ----------
        transition_states : list
            Lista de objetos tipo TransitionState.
        """
        self.__transition_states = self.__dict_items(transition_states)

    def add_transitions(self, transitions=[]):
        """ Agrega objetos tipo Transition dentro del modelo.

        Parameters
        ----------
        transitions : list
            Lista de objetos tipo Transition.
        """
        self.__transitions = self.__dict_items(transitions)
    
    def get_vesicles(self):
        """ Regresa el número total de vesiculas que se simulan en el modelo.
        
        Return
        ------
        int
            Número total de vesiculas en el modelo.
        """
        return self.__vesicles

    def get_transition_states(self):
        """ Regresa un diccionario con todos los objetos TransitionState definidos 
        dentro del modelo.

        Return
        ------
        dict
            Diccionario con los objetos tipo TransitionState del modelo.
        """
        return self.__transition_states

    def get_transitions(self):
        """ Regresa un diccionario con todos los objetos Transition definidos
        dentro del modelo.

        Return
        ------
        dict
            Diccionario con los objetos tipo Transition del modelo.
        """
        return self.__transitions

    def get_current_state(self):
        """ Regresa el nombre y el número de vesiculas en cada estado cinetico 
        vesicular en el presente.

        Return
        ------
        dict
            Diccionario con el nombre del cada estado cinetico vesicular como 
            key, y el número de vesiculas en dicho estado como value.
        """
        return {name: item.get_vesicles() for name, item in self.__transition_states.items()}

    def get_info(self):
        """ Regresa la información general del modelo.

        Return
        ------
        str
            Imprime el nombre del modelo, número total de vesiculas, nombre de 
            los TransitionState objects, nombre de los Transition objects y el 
            valor de los RateConstant objects.
        """
        print("="*16 + " MODEL INFORMATION " + "="*16)
        print(f"MODEL NAME:\t{self.get_name()}")
        print(f"TOTAL VESICLES:\t{self.__vesicles}")
        print(f"")
        print(f"TRANSITION STATES - VESICLES")
        for _, item in {**self.__transition_states, **self.__transitions}.items():
            item.get_info()
        print("="*52)

    def init(self):
        """ Inicializa el modelo y lo prepará antes de comenzar cualquier 
        experimento.
        """
        for _, value in self.__transition_states.items():
            value.update(self.__vesicles)
            break
        self.set_resting_state()

    def set_initial_state(self, dictionary_state):
        """ Establece un estado inicial para el modelo.

        Parameters
        ----------
        dictionary_state: dic
            Diccionario con el nombre de los objetos TransitionState 
            y el número de vesiculas en cada estado.
        """
        for name, state in self.__transition_states.items():
            state.update(dictionary_state[name])

    def set_resting_state(self):
        """ Establece el resting state del modelo.
        """
        self.__resting_state = self.get_current_state()

    def get_resting_state(self):
        """ Regresa los valores del modelo definido en el resting state.

        Return
        ------
        dict
            Diccionario con el resting state del modelo.
        """
        return self.__resting_state

    def get_graph(self):
        """ Genera un gráfo con la información del modelo. Es decir, el nombre
        del modelo, nombre de los estados de las transiciones vesiculares, las
        transitiones entre ellas, y el valor de las rate constants.
        """
        f = Digraph('Neuromuscular Synapse', 
                    filename='graph_model',
                    node_attr={'color': 'lightblue2', 'style': 'filled'}
                    )

        f.attr(rankdir='LR', size='8,5')
        f.attr('node', shape='doublecircle')

        for _, transition in self.__transitions.items():
            origin = list(transition.get_origin().keys())[0]
            destination = list(transition.get_destination().keys())[0]
            label = transition.get_rate_constant().get_name()
            
            if transition.get_rate_constant().get_stimulation():
                label = label + "*"

            f.edge(origin, destination, label=label)
        return f
        #f.view()
