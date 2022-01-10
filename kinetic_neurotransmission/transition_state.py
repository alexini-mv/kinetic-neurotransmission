from .neuromuscular import Synapse

class TransitionState(Synapse):
    """Se define el paso cinético dentro del módelo cinético vesicular presináptico.

    Methods
    -------
    update(vesicles)
        Setea el número de vesiculas totales que están en el paso cinético
    get_vesicles : int
        Regresa el número de vesiculas que están en este paso cinético
    add_vesicle(vesicles : int)
        Agrega vesicles a la población de vesiculas actuales del paso cinético
    pop_vesicle(vesicles : int)
        Disminuye vesicles a la población de vesiculas actuales del paso cinético.
    get_info
        Imprime la información general del paso cinético, tal como el nombre y el
        número de vesiculas actuales.
    """

    def __init__(self, name):
        """ Inicializamos el paso cinético del modelo cinético
        
        Parameters
        ----------
        name : str
            Nombre que tendrá el paso cinético
        """
        super().__init__(name)
        self.__vesicles = 0

    def update(self, vesicles):
        """Se setean el número total de vesiculas actuales que estarán en el 
        paso cinético

        Parameters
        ----------
        vesicles : int
            Numero total de vesicular que estarán en el paso cinético
        """
        self.__vesicles = vesicles

    def get_vesicles(self):
        """
        Returns
        -------
        int
            Número de vesiculas actuales en el paso cinético
        """
        return self.__vesicles

    def add_vesicle(self, vesicles):
        """
        Parameters
        ----------
        vesicles : int
            Número de vesiculas que se agregaran al total de vesiculas en el paso cinético
        """
        self.__vesicles += vesicles

    def pop_vesicle(self, vesicles):
        """
        Parameters
        ----------
        vesicles : int
            Número de vesiculas que se restaran al total de vesiculas en el paso cinético
        """
        self.__vesicles -= vesicles

    def get_info(self):
        """Imprime información del objeto TransitionState.
        
        Return
        ------
        str
            Información de los parametros definidos del objeto TransitionState.
        """
        print(f"{self.get_name()}\t:\t{self.get_vesicles()}")
