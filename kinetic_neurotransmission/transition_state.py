from .neuromuscular import Synapse

class TransitionState(Synapse):
    """Define el transition state dentro del modelo.

    Methods
    -------
    update()
        Actualiza el número de vesiculas que están en el TransitionState.
    get_vesicles()
        Regresa el número de vesiculas que están en el TransitionState.
    add_vesicle(vesicles : int)
        Agrega vesicles a la población de vesiculas actuales del TransitionState.
    pop_vesicle(vesicles : int)
        Disminuye vesicles a la población de vesiculas actuales del TransitionState.
    get_info()
        Imprime la información general del TransitionState object, tal como su 
        nombre y el número de vesiculas actuales.
    """

    def __init__(self, name):
        """ Inicializamos el transition state.
        
        Parameters
        ----------
        name : str
            Nombre del TransitionState object.
        """
        super().__init__(name)
        self.__vesicles = 0

    def update(self, vesicles):
        """Se actualiza el número total de vesiculas que estarán en el 
        TransitionState.

        Parameters
        ----------
        vesicles : int
            Numero total de vesiculas en TransitionState.
        """
        self.__vesicles = vesicles

    def get_vesicles(self):
        """ Regresa el número de vesiculas actuales que están en el TransitionState.
        Returns
        -------
        int
            Número de vesiculas en el TransitionState object.
        """
        return self.__vesicles

    def add_vesicle(self, vesicles):
        """ Agrega vesiculas dentro del TransitionState object.

        Parameters
        ----------
        vesicles : int
            Número de vesiculas que se agregaran al total de vesiculas en el 
            TransitionState object.
        """
        self.__vesicles += vesicles

    def pop_vesicle(self, vesicles):
        """ Quita vesicular del TransitionState object.

        Parameters
        ----------
        vesicles : int
            Número de vesiculas que se restaran al total de vesiculas en el 
            TransitionState.
        """
        self.__vesicles -= vesicles

    def get_info(self):
        """Imprime información general del objeto TransitionState.
        
        Return
        ------
        str
            Información de los attributos definidos del objeto TransitionState.
        """
        print(f"{self.get_name()}\t:\t{self.get_vesicles()}")
