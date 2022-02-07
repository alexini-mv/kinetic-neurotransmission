class Synapse:
    def __init__(self, name: str):
        self.__name: str = name

    def get_name(self):
        return self.__name

    def get_info(self):
        print("This is a element of synapse")
