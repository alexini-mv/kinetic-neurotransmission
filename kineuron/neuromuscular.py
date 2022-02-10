class Synapse:
    def __init__(self, name: str = None) -> None:
        self.__name: str = name

    def get_name(self) -> str:
        return self.__name

    def get_info(self) -> None:
        print("This is a element of synapse")
