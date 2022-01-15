from .neuromuscular import Synapse

class Transition(Synapse):
    """Defines a transition between two transition states.
    
    Methods
    -------
    get_origin()
        Returns a dictionary with the name of the source TransitionState object, 
        and the number of vesicles involved in the transition.
    get_destination()
        Returns a dictionary with the name of the destination TransitionState
        object, and the number of vesicles involved in the transition.
    get_rate_constant()
        Returns the RateConstant object associated with this Transition object.
    get_info()
        Returns the general information of the Transition object, i.e., its name, 
        the name and value of the associated RateConstant object, a flag 
        indicating whether the Transition object is calcium-dependent, as well 
        as the source and destination TransitionState involved in the Transition.
    """
    def __init__(self, name, rate_constant, origin={}, destination={}):
        """
        Parameters
        ----------
        name : str
            Transition object name.
        rate_constant : RateConstant object
            RateConstant object associated to the Transition object.
        origin : dict
            Dictionary with the name of the source TransitionState, and 
            the number of vesicles involved in the transition.
        destination : dict
            Dictionary with the name of the destination TransitionState, and 
            the number of vesicles involved in the transition.
        """
        super().__init__(name)
        self.__rate = rate_constant
        self.__origin = origin
        self.__destination = destination

    def get_rate_constant(self):
        """Returns the RateConstant object associated with this Transition.

        Return
        ------
        RateConstant object
        """
        return self.__rate 

    def get_origin(self):
        """Returns the source TransitionState information and the number of 
        vesicles involved in the Transition. 

        Return
        ------
        dict
            It includes the name information of the TransitionState object 
            source of the transition and the number of vesicles involved.
        """
        return self.__origin

    def get_destination(self):
        """Returns the destination TransitionState object information and 
        the number of vesicles involved in the Transition.

        Return
        ------
        dict
            It includes the name information of the TransitionState object 
            target of the transition and the number of vesicles involved.
        """
        return self.__destination

    def get_info(self):
        """Returns the general information of the Transition object.

        Return
        ------
        str
            Prints the name of the Transition object, the name of the 
            associated RateConstant object, as well as its numeric value and 
            whether it is calcium-dependent. It also prints the source and 
            destination TransitionState objects information.
        """
        print("-"*52)
        print(f"NAME:\t\t{self.get_name()}")
        self.__rate.get_info()
        print(f"ORIGIN:\t\t{self.__origin}")
        print(f"DESTINATION:\t{self.__destination}")

