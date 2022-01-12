from .neuromuscular import Synapse

class Transition(Synapse):
    """Define una transición entre dos transition states.
    
    Methods
    -------
    get_rate_constant()
        Regresa el objeto RateConstant asociado la Transition.
    get_origin()
        Regresa un diccionario donde está definido el nombre del TransitionState
        de origen, y el número de vesiculas que implicadas en la transition.
    get_destination()
        Regresa un diccionario donde está definido el nombre del TransitionState
        de destino, y el número de vesiculas implicada en la transition.
    get_info()
        Imprime la información general del objeto Transition. Es decir, 
        nombre, el nombre y el valor del RateConstant object asociado, una 
        bandera que indica si el Transition object es calcium-dependent, así como
        los TransitionState de origen y de destino implicados en el Transition.
    """
    def __init__(self, name, rate_constant, origin={}, destination={}):
        """
        Parameters
        ----------
        name : str
            Nombre con el cual se identificará la Transition.
        rate_constant : RateConstant object
            Objeto de la clase RateConstant asociado a la Transition.
        origin : dict
            Diccionario con el nombre del TransitionState de origen de el 
            número de vesiculas implicadas en la Transition.
        destination : dict
            Diccionario con el nombre del TransitionState de destino de el 
            número de vesiculas implicadas en la Transition.
        """
        super().__init__(name)
        self.__rate = rate_constant
        self.__origin = origin
        self.__destination = destination

    def get_rate_constant(self):
        """ Regresa el objeto RateConstant asociado a la Transition.

        Return
        ------
        RateConstant object
        """
        return self.__rate 

    def get_origin(self):
        """ Regresa la información de TransitionState origen y el número de 
        vesiculas que implicadas en la Transition.

        Return
        ------
        dict
            Incluye la información de nombre del TransitionState origen de la
            reacción y el número de vesiculas implicadas.
        """
        return self.__origin

    def get_destination(self):
        """ Regresa la información de TransitionState destino y el número de 
        vesiculas que implicadas en la Transition.

        Return
        ------
        dict
            Incluye la información de nombre del TransitionState destino de la
            reacción y el número de vesiculas implicadas.
        """
        return self.__destination

    def get_info(self):
        """ Imprime la información del objeto Transition.

        Return
        ------
        str
            Imprime el nombre del objeto Transition, el nombre del objeto 
            RateConstant asociado, así como su valor númerico y si es calcium-
            dependent. Igualmente, imprime la información del TransitionState 
            de origen y destino.
        """
        print("-"*52)
        print(f"NAME:\t\t{self.get_name()}")
        self.__rate.get_info()
        print(f"ORIGIN:\t\t{self.__origin}")
        print(f"DESTINATION:\t{self.__destination}")

