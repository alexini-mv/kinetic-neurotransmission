from graphviz import Digraph

from kineuron import transition_state

from .neuromuscular import Synapse


class KineticModel(Synapse):
    """Defines the kinetic model for modeling vesicle maturation transitions
    at the neuromuscular junction.

    Attributs
    ---------
    _init_resting_state : bool
        If is True, it indicates that the initial kinetic state of the model
        is the resting state. Otherwise, the initial state is other.

    vesicles : int
        Total number of vesicles simulated in the kinetic model.

    transitions : dict
        Dictionary with the name and values of the kineuron.Transition objects
        defined in the model.

    transition_states : dict
        Dictionary with the name and values of the kineuron.TransitionState
        objects defined in the model.


    Methods
    -------
    add_transitions
        Adds to the model a list of all the kineuron.Transitions objects between
        the kineuron.TransitionState objects within the model.

    add_transition_states
        Adds to the model a list of all the kineuron.TransitionState objects
        that constitute the model.

    get_current_state
        Returns a dictionary with the name and number of instantaneous vesicles
        in each of the kineuron.TransitionState objects defined in the model.

    get_graph
        It generates a graph with the model information, i.e. the name of
        the vesicular kinetic states, transitions and rate constants.

    get_info
        Prints the general information of the model, i.e. the name and status
        of the kineuron.TransitionState, kineuron.Transition,
        kineuron.RateConstant objects.

    get_resting_state
        Returns a dictionary with the name and number of vesicles in each
        kineuron.TransitionState object corresponding to the model resting
        state.

    get_transitions
        Returns a list of all kineuron.Transition objects defined in the model.

    get_transition_states
        Returns a list of all kineuron.TransitionState object defined within
        the model.

    get_vesicle
        Returns the total number of vesicles that are simulated in the model.

    init
        Initializes the model with the added objects and prepares it to start
        the simulation.

    set_initial_state
        An initial state of the model is established (name and number of
        vesicles in each kineuron.TransitionState object) from which the model
        will be simulated.

    set_resting_state
        Sets the model resting state.
    """

    def __init__(self, name: str = "Kinetic Model", vesicles: int = 10000):
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
        self._init_flag: bool = None
        self._init_resting_state: bool = None
        self.__vesicles: int = vesicles
        self.__transitions: dict = None
        self.__transition_states: dict = None

    def __dict_items(self, list_items: list) -> dict:
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

    def add_transition_states(self, transition_states: list) -> None:
        """Adds a list of kineuron.TransitionState objects inside the model.

        Parameters
        ----------
        transition_states : list
            List of kineuron.TransitionState objects.
        """
        self.__transition_states: dict = self.__dict_items(transition_states)

    def add_transitions(self, transitions: list) -> None:
        """Adds a list of kineuron.Transition objects inside the model.

        Parameters
        ----------
        transitions : list
            List of kineuron.Transition objects.
        """
        self.__transitions: dict = self.__dict_items(transitions)

    def get_vesicles(self) -> int:
        """Returns the total number of vesicles simulated in the model.

        Return
        ------
        int
            Total number of vesicles in the model.
        """
        return self.__vesicles

    def get_transition_states(self) -> dict:
        """Returns a dictionary with all the kineuron.TransitionState objects
        defined within the model.

        Return
        ------
        dict
            A dictionary with all kineuron.TransitionState objects.
        """
        return self.__transition_states

    def get_transitions(self) -> dict:
        """Returns a dictionary with all the kineuron.Transition objects
        defined within the model.

        Return
        ------
        dict
            Dictionary with kineuron.Transition objects of the model.
        """
        return self.__transitions

    def get_current_state(self) -> dict:
        """Returns the name and number of vesicles in each
        kineuron.TransitionState in the current state of the model.

        Return
        ------
        dict
            Dictionary with the name of each kineuron.TransitionState and the
            number of vesicles in that state.
        """
        return {name: item.get_vesicles() for name, item in self.__transition_states.items()}

    def __str__(self) -> str:
        """Builds a string with general information of the model.

        Return
        ------
        str
            Name model, the total number of vesicles and the
            information of the kineuron.TransitionState, kineuron.Transition
            and kineuron.RateConstant objects.
        """
        width = 50
        left = 30

        msg = ["", "  MODEL INFORMATION  ".center(width, "="),
               "MODEL NAME:".ljust(left) + self.get_name(),
               "TOTAL VESICLES:".ljust(left) + str(self.__vesicles),
               "RESTING STATE:".ljust(left) + str(self._init_resting_state),
               "", "TRANSITION STATES".ljust(left) + "VESICLES"]

        if self.__transition_states is not None and self.__transitions is not None:
            for _, item in {**self.__transition_states, **self.__transitions}.items():
                msg.append(str(item))

        msg.append("".center(width, "="))

        return "\n".join(msg)

    def get_info(self) -> None:
        """Returns the general information of the model.

        Return
        ------
            Prints the model name, the total number of vesicles and the
            information of the kineuron.TransitionState, kineuron.Transition
            and kineuron.RateConstant objects.
        """
        print(self.__str__())

    def init(self) -> None:
        """Initializes the model and prepares it before running any simulation.
        """
        for i, value in enumerate(self.__transition_states.values()):
            if i == 0:
                value.update(self.__vesicles)
            else:
                value.update(0)

        self.set_resting_state()

        self._init_flag: bool = True
        self._init_resting_state: bool = False

        print("Model initialized")

    def set_initial_state(self, dictionary_state: dict) -> None:
        """Sets a particular initial state for the model.

        Parameters
        ----------
        dictionary_state: dict
            Dictionary with the name of all kineuron.TransitionState objects
            and the number of vesicles in each state.
        """
        for name, state in self.__transition_states.items():
            state.update(dictionary_state[name])

    def set_resting_state(self) -> None:
        """Sets the model resting state.
        """
        self.__resting_state = self.get_current_state()

    def get_resting_state(self) -> dict:
        """Returns the values of the model defined in its resting state.

        Return
        ------
        dict
            Dictionary with the model resting state.
        """
        return self.__resting_state

    def get_graph(self) -> Digraph:
        """Generates a graph with the model information, i.e., the model name, 
        the names of the kineuron.TransitionState, the kineuron.Transitions 
        between them and the value of their corresponding rate constants.

        Return
        ------
        graphviz.Digraph
            Graph with kinetic model.
        """
        f = Digraph('Kinetic Model of Neuromuscular Transmission',
                    filename='graph_model',
                    node_attr={'color': 'lightblue2', 'style': 'filled'}
                    )
        f.attr(rankdir='LR', size='8,5')
        f.attr('node', shape='doublecircle')

        for _, transition in self.__transitions.items():
            origin = transition.get_origin()
            destination = transition.get_destination()
            label = transition.get_rate_constant().get_name()

            if transition.get_rate_constant().get_calcium_dependent():
                label = label + "*"

            f.edge(origin, destination, label=label)

        return f
