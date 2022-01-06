from .synapse import Synapse

class Reaction(Synapse):
    """Se define las reacciones entre dos estados cinéticos vesiculares presinapticos
    
    Methods
    -------
    get_rate_reaction
        Regresa el objeto rate_reaction asociado la transición cinética
    get_origin
        Regresa un diccionario donde está definido el nombre del paso cinético
        de origen de la transición
    get_destination
        Regresa un diccionario donde está definido el nombre del paso cinético
        de destino de la transición
    get_info
        Imprime la información general del objeto Reaction, por ejemplo su 
        nombre, el nombre y el valor de la constante de reacción asociada,
        también si el valor constante es afectada por estimulación externa,
        el paso cinético de origen y de destino de la reacción
    """
    def __init__(self, name, rate, origin={}, destination={}):
        """
        Parameters
        ----------
        name : str
            Nombre con el cual se identificará la reacción
        rate : rate_reaction object
            Objeto de la clase RateReaction asociado a la reacción
        origin : dict
            Diccionario con Key como el nombre del paso cinético de origen de
            la transición cinética y Value el número de vesiculas implicadas en
            dicha transición.
        destination : dict
            Diccionario con Key como el nombre del paso cinético de destino
            de la transición cinética y Value el número de vesiculas implicadas
            en dicha transición.
        """
        super().__init__(name)
        self.__rate = rate
        self.__origin = origin
        self.__destination = destination

    def get_rate_reaction(self):
        """ Regresa el objeto RateReaction asociado a la reacción.

        Return
        ------
        rate_reaction object
        """
        return self.__rate 

    def get_origin(self):
        """ Regresa la información de estado vesicular origen y el número de 
        vesiculas que transitan por cada reacción.

        Return
        ------
        dict
            Incluye la información de nombre del kinetic_state origen de la
            reacción, así como el número de vesiculas que transitan.
        """
        return self.__origin

    def get_destination(self):
        """ Regresa la información de estado vesicular destination y el número
        de vesiculas que transitan por cada reacción.

        Return
        ------
        dict
            Incluye la información de nombre del kinetic_state destino de la
            reacción, así como el número de vesiculas que transitan.
        """
        return self.__destination

    def get_info(self):
        """ Imprime la información del objeto reaction.

        Return
        ------
        str
            Imprime el nombre del objeto reaction, el nombre del objeto velocidad
            de reacción asociado así como su valor númerico. También imprime si
            dicha velocidad de reacción será afectada por estimulación externa. 
            Y finalmente imprime el estado cinético de origen y destino de la
            reacción.
        """
        print("="*50)
        print(f"NAME:\t\t{self.get_name()}")
        print(f"RATE NAME:\t{self.__rate.get_name()}")
        print(f"RATE VALUE:\t{self.__rate.get_rate()}")
        print(f"STIMULATION:\t{self.__rate.get_stimulation()}")
        print(f"ORIGIN:\t\t{self.__origin}")
        print(f"DESTINATION:\t{self.__destination}")

