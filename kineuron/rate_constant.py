from .neuromuscular import Synapse

class RateConstant(Synapse):
    """Defines the object that will store the rate constant information 
    associated to each Transition object.

    Methods
    -------
    get_rate : float
        Returns the numerical value of the rate constant.
    get_calcium_dependent : bool
        Returns True if the rate constant is affected by the stimulation. 
        Otherwise, it returns False.
    get_info: str
        Returns the general information of the object, i.e. the name of the 
        RateConstant, its numerical value and whether it is affected by 
        stimulation.
    """
    def __init__(self, name, value, calcium_dependent=False):
        """
        Parameters
        ----------
        name : str
            Name of rate constant.
        value : float
            Value of the rate constant.
        calcium_dependent : bool, optional
            Flag to indicate if this rate constant is affected by 
            stimulation. Default is False.
        """
        super().__init__(name)
        self.__rate = value
        self.__calcium_dependent = calcium_dependent
        
    def get_rate(self):
        """Returns the numerical value of the rate constant.

        Return
        ------
        float
            Value of the rate constant.
        """
        return self.__rate

    def get_calcium_dependent(self):
        """Flag to indicate if this rate constant is affected by stimulation.

        Return
        ------
        bool
            Returns True if the rate constant is affected by the stimulation. 
            Otherwise, returns False.
        """
        return self.__calcium_dependent

    def get_info(self):
        """Returns the general information of the RateConstant object, i.e. 
        its name, the numerical value of the rate constant and whether it 
        is affected by stimulation.

        Return
        ------
        str
            General information about the RateConstant object.
        """
        print(f"RATE CONSTANT NAME:\t{self.get_name()}")
        print(f"RATE CONSTANT VALUE:\t{self.get_rate()} s⁻¹")
        print(f"CALCIUM-DEPENDENT:\t{self.get_calcium_dependent()}")
