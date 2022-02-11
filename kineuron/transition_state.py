from .neuromuscular import Synapse


class TransitionState(Synapse):
    """Defines a transition state of the model.

    Methods
    -------
    update
        Updates the number of vesicles that are in the kineuron.TransitionState
        object.
    get_vesicle
        Returns the number of vesicles that are in the kineuron.TransitionState 
        object.
    add_vesicle
        Add a vesicle to the current kineuron.TransitionState vesicle population.
    pop_vesicle
        Drop a vesicle to the current vesicle population of the 
        kineuron.TransitionState object.
    get_info
        Returns the general information of the kineuron.TransitionState object, 
        such as its name and the number of current vesicles.
    """

    def __init__(self, name: str) -> None:
        """
        Parameters
        ----------
        name : str
            kineuron.TransitionState object name.
        """
        super().__init__(name)
        self.__vesicles: int = 0

    def get_vesicles(self) -> int:
        """ Returns the number of current vesicles that are in the 
        kineuron.TransitionState object.

        Returns
        -------
        int
            Number of vesicles in the kineuron.TransitionState object.
        """
        return self.__vesicles

    def update(self, vesicles: int) -> None:
        """Updates the total number of vesicles that are in the
        kineuron.TransitionState object.

        Parameters
        ----------
        vesicles : int
            Total number of vesicles in the kineuron.TransitionState object.
        """
        self.__vesicles = vesicles

    def add_vesicle(self, vesicles: int = 1) -> None:
        """Add a vesicle to the current kineuron.TransitionState vesicle 
        population.

        Parameters
        ----------
        vesicles : int, optional
            Number of vesicles to be added.
        """
        self.__vesicles += vesicles

    def pop_vesicle(self, vesicles: int = 1) -> None:
        """Remove a vesicle from the kineuron.TransitionState vesicle 
        population.

        Parameters
        ----------
        vesicles : int, optional
            Number of vesicles to be removed.
        """
        self.__vesicles -= vesicles

    def __str__(self) -> str:
        """Builds a string with the general information of the 
        kineuron.TransitionState object.

        Return
        ------
        str
            Name of the kineuron.TransitionState object and its number of 
            vesicles.
        """
        return f"{self.get_name()}:".ljust(30) + str(self.get_vesicles())

    def get_info(self) -> None:
        """Returns the general information of the kineuron.TransitionState 
        object.

        Return
        ------
            Name of the kineuron.TransitionState object and its number of 
            vesicles.
        """
        print(self.__str__())
