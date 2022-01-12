from .neuromuscular import Synapse

class RateConstant(Synapse):
    """Define el objeto que guarda la información de la rate constant asociada
    a cada Transition object.

    Methods
    -------
    get_rate : float
        Regresa el valor numérico de la rate constant.
    get_calcium_dependent : bool
        Regresa un True si la rate constant es influenciada durante la estimulación. 
        En caso contrario, regresa un False.
    get_info: str
        Imprime la información general del objeto, es decir, el nombre de la 
        RateConstant, su valor numérico y si es afectada por la estimulación.
    """
    def __init__(self, name, value, calcium_dependent=False):
        """
        Parameters
        ----------
        name : str
            Nombre de la rate constant.
        value : float
            Valor que tiene la rate constant.
        calcium_dependent : bool, optional
            Una bandera para indicar si está constante de reacción es influenciada
            por la estimulación. Default is False.
        """
        super().__init__(name)
        self.__rate = value
        self.__calcium_dependent = calcium_dependent
        
    def get_rate(self):
        """ Regresa el valor númerico de la rate constant.

        Return
        ------
        float
            Valor númerico de la rate constant.
        """
        return self.__rate

    def get_calcium_dependent(self):
        """ Bandera que indica si la velocidad de reacción es influenciada
        por la función de estimulación.

        Return
        ------
        bool
            Regresará True la rate constant será afectada por la estimulación. 
            En caso contrario, regresará False.
        """
        return self.__calcium_dependent

    def get_info(self):
        """ Imprime la información del objeto RateConstant, es decir, su nombre, el valor 
        númerico de la rate constant y si es afectada por estimulación.

        Return
        ------
        str
            Información del objeto RateConstant.
        """
        print(f"RATE CONSTANT NAME:\t{self.get_name()}")
        print(f"RATE CONSTANT VALUE:\t{self.get_rate()} s⁻¹")
        print(f"CALCIUM-DEPENDENT:\t{self.get_calcium_dependent()}")
