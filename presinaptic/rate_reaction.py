from .synapse import Synapse

class RateReaction(Synapse):
    """Define el objeto que guarda la información de la velocidad de reacción.

    Methods
    -------
    get_rate : float
        Regresa el valor numérico de la constate de reacción
    get_stimulation : bool
        Regresa un True si la constante cambia de valor durante la estimulación,
        en caso contrario, regresa un False
    get_info
        Imprime la información general del objeto, como es el nombre de la 
        constante de reacción, su valor y si es afectada por la estimulación
    """
    def __init__(self, name, rate, stimulation=False):
        """
        Parameters
        ----------
        name : str
            Nombre de la constante de reacción
        rate : float
            Valor que tendrá la constante de reacción
        stimulation : bool, optional
            Una bandera para indicar si está constante de reacción será afectada
            por la estimulación de la sinapsis. Default is False
        """
        super().__init__(name)
        self.__rate = rate
        self.__stimulation = stimulation
        
    def get_rate(self):
        """ Regresa el valor númerico de la velocidad de reacción.

        Return
        ------
        int
            Valor de la velocidad de reacción.
        """
        return self.__rate

    def get_stimulation(self):
        """ Bandera que indica si la velocidad de reacción será afectada por 
        una función de estimulación.

        Return
        ------
        bool
            Regresará true la velocidad de reacción será afectada por la 
            estimulación. En caso contrario, regresará false.
        """
        return self.__stimulation

    def get_info(self):
        """ Imprime el nombre del objeto, el valor númerico de la velocidad de
        la velocidad de reacción y si es afectada por estimulación externa.

        Return
        ------
        str
            Información del objeto rate_reaction.
        """
        print("-"*50)
        print(f"NAME:\t{self.get_name()}")
        print(f"RATE:\t{self.get_rate()}")
        print(f"STIMULATION:\t{self.get_stimulation()}")
