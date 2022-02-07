from .neuromuscular import Synapse

class TransitionState(Synapse):
    """Defines a transition state of the model.

    Methods
    -------
    update()
        Updates the number of vesicles that are in the TransitionState object.
    get_vesicles()
        Returns the number of vesicles that are in the TransitionState object.
    add_vesicle(vesicles : int)
        Adds vesicles to the current TransitionState vesicle population.
    pop_vesicle(vesicles : int)
        Drop vesicles to the current vesicle population of the 
        TransitionState object.
    get_info()
        Returns the general information of the TransitionState object, such as 
        its name and the number of current vesicles.
    """

    def __init__(self, name):
        """
        Parameters
        ----------
        name : str
            TransitionState object name.
        """
        super().__init__(name)
        self.__vesicles = 0

    def get_vesicles(self):
        """ Returns the number of current vesicles that are in the 
        TransitionState object.

        Returns
        -------
        int
            Number of vesicles in the TransitionState object.
        """
        return self.__vesicles

    def update(self, vesicles):
        """Updates the total number of vesicles that are in the 
        TransitionState object.

        Parameters
        ----------
        vesicles : int
            Total number of vesicles in the TransitionState object.
        """
        self.__vesicles = vesicles

    def add_vesicle(self, vesicles):
        """Adds vesicles to the current TransitionState vesicle population.

        Parameters
        ----------
        vesicles : int
            Number of vesicles to be added.
        """
        self.__vesicles += vesicles

    def pop_vesicle(self, vesicles):
        """ Remove vesicular from the TransitionState object.

        Parameters
        ----------
        vesicles : int
            Number of vesicles to be removed.
        """
        self.__vesicles -= vesicles

    def get_info(self):
        """Returns the general information of the TransitionState object.
        
        Return
        ------
        str
            Name of the TransitionState object and its number of vesicles.
        """
        print(f"{self.get_name()}\t:\t{self.get_vesicles()}")
