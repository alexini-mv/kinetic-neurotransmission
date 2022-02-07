from graphviz import Digraph

from .neuromuscular import Synapse


class KineticModel(Synapse):
    """Defines the kinetic model for modeling vesicle maturation transitions 
    at the neuromuscular junction.

    Attributs
    ---------
    vesicles : int
        Total number of vesicles simulated in the kinetic model.
    transition_states : dict
        Dictionary with the name and values of the TransitionState objects 
        defined in the model.
    transitions : dict
        Dictionary with the name and values of the Transition objects defined 
        in the model.
    rates : dict
        Dictionary with the name and values of the RateConstant objects 
        associated to each Transition object within the model.

    Methods
    -------
    add_rate_constants(rates : list)
        Adds to the model a list of all RateConstant objects of each vesicular 
        kinetic transition.
    add_transition_states(transition_states : list)
        Adds to the model a list of all the TransitionState objects that 
        constitute the model.
    add_transitions(transitions : list)
        Adds to the model a list of all the Transitions objects between the 
        TransitionState objects within the model.
    get_vesicle
        Returns the total number of vesicles that are simulated in the model.
    get_transition_states
        Returns a list of all TransitionState object defined within the model.
    get_transitions
        Returns a list of all Transition objects defined in the model.
    get_current_state
        Returns a dictionary with the name and number of instantaneous vesicles
        in each of the TransitionState objects defined in the model.
    get_info
        Prints the general information of the model, i.e. the name and status 
        of the TransitionState, Transition, RateConstant objects.
    init
        Initializes the model with the added objects and prepares it to start 
        the simulation.
    set_initial_state(dictionary_state : dict)
        An initial state of the model is established (name and number of 
        vesicles in each TransitionState object) from which the model will be 
        simulated.
    set_resting_state
        Sets the model resting state.
    get_resting_state
        Returns a dictionary with the name and number of vesicles in each 
        TransitionState object corresponding to the model resting state.
    get_graph
        It generates a graph with the model information, i.e. the name of 
        the vesicular kinetic states, transitions and rate constants.
    """

    def __init__(self, name="Kinetic Model", vesicles=10000):
        """The kinetic model is initialized to simulate the transitions 
        between different vesicular states.

        Parameters
        ----------
        name : str, optional
            Model name.
        vesicles : int, optional
            Total number of vesicles to be simulated in the model.
        """
        super().__init__(name)
        self.__vesicles = vesicles

    def __dict_items(self, list_items):
        """Auxiliary function to convert a list of items to a dictionary.

        Parameters
        ----------
        list_items : list
            List of items to be converted into a dictionary.

        Return
        ------
        dict
            Dictionary with the name of each item and the object.
        """
        return {item.get_name(): item for item in list_items}

    def add_rate_constants(self, rates=[]):
        """Adds a list of RateConstant objects inside the model.

        Parameters
        ----------
        rates : list
            List of RateConstant objects.
        """
        self.__rates = self.__dict_items(rates)

    def add_transition_states(self, transition_states=[]):
        """Adds a list of TransitionState objects inside the model.

        Parameters
        ----------
        transition_states : list
            List of TransitionState objects.
        """
        self.__transition_states = self.__dict_items(transition_states)

    def add_transitions(self, transitions=[]):
        """Adds a list of Transition objects inside the model.

        Parameters
        ----------
        transitions : list
            List of Transition objects.
        """
        self.__transitions = self.__dict_items(transitions)

    def get_vesicles(self):
        """Returns the total number of vesicles simulated in the model.

        Return
        ------
        int
            Total number of vesicles in the model.
        """
        return self.__vesicles

    def get_transition_states(self):
        """Returns a dictionary with all the TransitionState objects 
        defined within the model.

        Return
        ------
        dict
            A dictionary with all the TransitionState objects.
        """
        return self.__transition_states

    def get_transitions(self):
        """Returns a dictionary with all the Transition objects 
        defined within the model.

        Return
        ------
        dict
            Dictionary with the Transition objects of the model.
        """
        return self.__transitions

    def get_current_state(self):
        """Returns the name and number of vesicles in each TransitionState 
        in the current state of the model.

        Return
        ------
        dict
            Dictionary with the name of each TransitionState and the number of 
            vesicles in that state.
        """
        return {name: item.get_vesicles() for name, item in self.__transition_states.items()}

    def get_info(self):
        """Returns the general information of the model.

        Return
        ------
        str
            Prints the model name, including the total number of vesicles, and 
            the information of the TransitionState, Transition and RateConstant objects.
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
        """Initializes the model and prepares it before running any simulation.
        """
        for _, value in self.__transition_states.items():
            value.update(self.__vesicles)
            break
        self.set_resting_state()

    def set_initial_state(self, dictionary_state):
        """Sets a particular initial state for the model.

        Parameters
        ----------
        dictionary_state: dic
            Dictionary with the name of all TransitionState objects and the 
            number of vesicles in each state.
        """
        for name, state in self.__transition_states.items():
            state.update(dictionary_state[name])

    def set_resting_state(self):
        """Sets the model resting state.
        """
        self.__resting_state = self.get_current_state()

    def get_resting_state(self):
        """Returns the values of the model defined in its resting state.

        Return
        ------
        dict
            Dictionary with the model resting state.
        """
        return self.__resting_state

    def get_graph(self):
        """Generates a graph with the model information, i.e., the model name, 
        the names of the TransitionsState, the transitions between them, and the 
        value of their corresponding rate constants.
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

            if transition.get_rate_constant().get_calcium_dependent():
                label = label + "*"

            f.edge(origin, destination, label=label)
        return f
