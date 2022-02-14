class Synapse:
    def __init__(self, name: str = None) -> None:
        self.__name: str = name

    def get_name(self) -> str:
        """Returns the user-defined name of the instantiated object."""
        return self.__name

    def get_info(self) -> None:
        """Returns the general information of the object."""
        print("This is a element of synapse")
