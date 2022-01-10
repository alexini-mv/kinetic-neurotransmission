from graphviz import Digraph
from .neuromuscular import Synapse

class KineticModel(Synapse):
    """Se define el modelo cinético para modelar las fases de 
    maduración de las vesículas en la terminal sináptica nerviosa.

    Attributs
    ---------
    vesicles : int
        Número de vesiculas totales que se simularán en el modelo cinético.
    transition_states : dict
        Diccionario con el nombre y valores de los objetos transition_state del modelo.
    transitions : dict
        Diccionario con el nombre y valores de los objetos reaction del modelo.
    rates : dict
        Diccionario con el nombre y valores de los objetos velocidades de transición 
        entre los kinetic_state vesiculares del modelo.

    Methods
    -------
    add_rate_constants(rates : list)
        Agrega al modelo la lista de todos los objetos velocidades de cada
        transición cinética vesicular.
    add_transition_states(transition_states : list)
        Agrega al modelo la lista de todos los objetos transition_state que componen
        al modelo.
    add_transitions(transitions : list)
        Agrega al modelo la lista de todas las reacciones entre los kinetic_state 
        del modelo.
    get_vesicle
        Imprime el numero total de vesiculas que se están simulando en el modelo.
    get_transition_states
        Regresa una lista con todos los estados cinéticos definidos en el 
        modelo.
    get_transitions
        Regresa una lista con todos las reacciones entre estados cinéticos 
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
        Se define el attribut privado resting_state que guardará el estado 
        resting del modelo.
    get_resting_state
        Regresa un diccionario con el nombre y el número de vesiculas en cada
        estado cinético vesicular correspondiente al resting state del modelo.
    get_graph
        Regresa un grafo con la información de modelo, es decir, el nombre de 
        los estados cinéticos vesiculares, reacciones y velocidades de reacción.
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
        """ Función auxiliar para convertir una lista de items a un diccionario
        
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
        """ Agrega una lista de objetos tipo rate_reaction al modelo.

        Parameters
        ----------
        rates : list
            Lista de objetos tipo rate_reaction.
        """
        self.__rates = self.__dict_items(rates)

    def add_transition_states(self, transition_states=[]):
        """ Agrega una lista de objetos tipo kinetic_state al modelo.

        Parameters
        ----------
        transition_states : list
            Lista de objetos tipo kinetic_state.
        """
        self.__transition_states = self.__dict_items(transition_states)

    def add_transitions(self, transitions=[]):
        """ Agrega una lista de objetos tipo reaction al modelo.

        Parameters
        ----------
        transitions : list
            Lista de objetos tipo reaction.
        """
        self.__transitions = self.__dict_items(transitions)
    
    def get_vesicles(self):
        """ Imprime el número de vesiculas totales que se simulan en el modelo.
        
        Return
        ------
        int
            Número de vesiculas totales en el modelo.
        """
        return self.__vesicles

    def get_transition_states(self):
        """ Regresa un diccionario con todos los objetos kinetic_state en el 
        modelo.

        Return
        ------
        dict
            Diccionario con todos los objetos del tipo kinetic_state del modelo.
        """
        return self.__transition_states

    def get_transitions(self):
        """ Regresa un diccionario con todos los objetos reaction en el 
        modelo.

        Return
        ------
        dict
            Diccionario con todos los objetos del tipo reaction del modelo.
        """
        return self.__transitions

    def get_current_state(self):
        """ Regresa el nombre y el número de vesiculas en cada estado cinetico 
        vesicular en el presente.

        Return
        ------
        dict
            Diccionario con el nombre del cada estado cinetico vesicular como 
            key, y el número de vesiculas como value.
        """
        return {name: item.get_vesicles() for name, item in self.__transition_states.items()}

    def get_info(self):
        """ Regresa la información general del modelo.

        Return
        ------
        str
            Información general definida dentro del modelo: Nombre del modelo, 
            número total de vesicular, nombre de los estados cinéticos 
            vesiculares, nombre de las reacciones y el valor de las velocidades
            de reacción.
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
        """ Inicializa el modelo con el número de vesiculas y los estados 
        cinéticos.
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
            Diccionario con el nombre de objetos tipo estados cinéticos 
            y el número de vesiculas particular en cada estado.
        """
        for name, state in self.__transition_states.items():
            state.update(dictionary_state[name])

    def set_resting_state(self):
        """ Guarda el estado estacionario del modelo.
        """
        self.__resting_state = self.get_current_state()

    def get_resting_state(self):
        """ Regresa los valores del estado estacionario del modelo.
        Return
        ------
        dict
            Diccionario con el estado estacionario del modelo.
        """
        return self.__resting_state

    def get_graph(self):
        """ Genera un grafo con la información del modelo. Es decir, el nombre
        del modelo, nombre de los estados cinéticos vesiculares, reacciones
        cinéticas entre ellos, y el valor de las velocidades de cada reacción.
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
