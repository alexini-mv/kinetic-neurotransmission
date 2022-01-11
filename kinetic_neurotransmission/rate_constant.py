from .neuromuscular import Synapse

class RateConstant(Synapse):
    """Define el objeto que guarda la información de la velocidad de reacción.

    Methods
    -------
    get_rate : float
        Regresa el valor numérico de la constate de reacción
    get_calcium_dependent : bool
        Regresa un True si la constante cambia de valor durante la estimulación,
        en caso contrario, regresa un False
    get_info
        Imprime la información general del objeto, como es el nombre de la 
        constante de reacción, su valor y si es afectada por la estimulación
    """
    def __init__(self, name, value, calcium_dependent=False):
        """
        Parameters
        ----------
        name : str
            Nombre de la constante de reacción
        value : float
            Valor que tendrá la constante de reacción
        calcium_dependent : bool, optional
            Una bandera para indicar si está constante de reacción será afectada
            por la estimulación de la sinapsis. Default is False
        """
        super().__init__(name)
        self.__rate = value
        self.__calcium_dependent = calcium_dependent
        
    def get_rate(self):
        """ Regresa el valor númerico de la velocidad de reacción.

        Return
        ------
        int
            Valor de la velocidad de reacción.
        """
        return self.__rate

    def get_calcium_dependent(self):
        """ Bandera que indica si la velocidad de reacción será afectada por 
        una función de estimulación.

        Return
        ------
        bool
            Regresará true la velocidad de reacción será afectada por la 
            estimulación. En caso contrario, regresará false.
        """
        return self.__calcium_dependent

    def get_info(self):
        """ Imprime el nombre del objeto, el valor númerico de la velocidad de
        la velocidad de reacción y si es afectada por estimulación externa.

        Return
        ------
        str
            Información del objeto rate_constant.
        """
        print("-"*50)
        print(f"NAME:\t\t{self.get_name()}")
        print(f"RATE CONSTANT:\t{self.get_rate()} s⁻¹")
        print(f"CALCIUM-DEPENDENT:\t{self.get_calcium_dependent()}")
