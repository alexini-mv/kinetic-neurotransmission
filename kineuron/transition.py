from .neuromuscular import Synapse
from .rate_constant import RateConstant


class Transition(Synapse):
    """Defines a transition between two transition states.

    Methods
    -------
    get_origin
        Returns a dictionary with the name of the source 
        kineuron.TransitionState object and the number of vesicles involved in 
        the transition.
    get_destination
        Returns a dictionary with the name of the destination 
        kineuron.TransitionState object, and the number of vesicles involved in
        the transition.
    get_rate_constant
        Returns the kineuron.RateConstant object associated with this 
        kineuron.Transition object.
    get_info
        Returns the general information of the kineuron.Transition object, 
        i.e., its name, the name and value of the associated RateConstant 
        object, a flag indicating whether the kineuron.Transition object is 
        calcium-dependent, as well as the source and destination 
        kineuron.TransitionState involved in this kineuron.Transition.
    """

    def __init__(self, name: str, rate_constant: RateConstant,
                 origin: str, destination: str) -> None:
        """
        Parameters
        ----------
        name : str
            Transition object name.
        rate_constant : kineuron.RateConstant object
            kineuron.RateConstant object associated to the kineuron.Transition 
            object.
        origin : str
            Name of the source kineuron.TransitionState involved in the 
            transition.
        destination : str
            Name of the destination kineuron.TransitionState involved in the 
            transition.
        """
        super().__init__(name)
        self.__rate: RateConstant = rate_constant
        self.__origin: str = origin
        self.__destination: str = destination

    def get_rate_constant(self) -> RateConstant:
        """Returns the kineuron.RateConstant object associated with this 
        kineuron.Transition.

        Return
        ------
        kineuron.RateConstant
        """
        return self.__rate

    def get_origin(self) -> str:
        """Returns name of source kineuron.TransitionState involved in this 
        kineuron.Transition. 

        Return
        ------
        str
            Name of the kineuron.TransitionState object source of the transition
            involved.
        """
        return self.__origin

    def get_destination(self) -> str:
        """Returns name of destination kineuron.TransitionState involved in the
        kineuron.Transition.

        Return
        ------
        str
            Name of the kineuron.TransitionState object target of the transition
            involved.
        """
        return self.__destination

    def __str__(self) -> str:
        """Builds a string with the general information of the 
        kineuron.Transition object.

        Return
        ------
        str
            Name of the kineuron.Transition object, the name of the associated
            kineuron.RateConstant object, as well as its numeric value and 
            whether it is calcium-dependent. It also includes the source and 
            destination kineuron.TransitionState objects information.
        """
        width = 50
        left = 30
        msg = [
            "".center(width, "-"),
            "NAME TRANSITION:".ljust(left) + self.get_name(),
            str(self.__rate),
            "ORIGIN:".ljust(left) + self.__origin,
            "DESTINATION:".ljust(left) + self.__destination
        ]
        return "\n".join(msg)

    def get_info(self) -> None:
        """Returns the general information of the kineuron.Transition object.

        Return
        ------
            Prints the name of the kineuron.Transition object, the name of the
            associated kineuron.RateConstant object, as well as its numeric 
            value and whether it is calcium-dependent. It also prints the 
            source and destination kineuron.TransitionState objects information.
        """
        print(self.__str__())
