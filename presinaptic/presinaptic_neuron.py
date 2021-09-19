from graphviz import Digraph
from .synapse import Synapse

class PresinapticNeuron(Synapse):
    def __init__(self, name, vesicles=1000):
        super().__init__(name)
        self.__vesicles = vesicles

    def __dict_items(self, list_items):
        return {item.get_name(): item for item in list_items}

    def add_rate_reactions(self, rates=[]):
        self.__rates = self.__dict_items(rates)

    def add_kinetic_states(self, kinetic_states=[]):
        self.__kinetic_states = self.__dict_items(kinetic_states)

    def add_reactions(self, reactions=[]):
        self.__reactions = self.__dict_items(reactions)
    
    def get_vesicles(self):
        return self.__vesicles

    def get_kinetic_states(self):
        return self.__kinetic_states

    def get_reactions(self):
        return self.__reactions

    def get_current_state(self):
        return {name: item.get_vesicles() for name, item in self.__kinetic_states.items()}

    def get_info(self):
        print("*"*15 + " SYNAPSE INFORMATION " + "*"*15)
        print(f"NAME SYNAPSE:\t{self.get_name()}")
        print(f"TOTAL VESICLES:\t{self.__vesicles}")
        print(f"")
        for _, item in {**self.__kinetic_states, **self.__reactions}.items():
            item.get_info()
        print("*"*50)

    def init(self):
        for _, value in self.__kinetic_states.items():
            value.update(self.__vesicles)
            break
        self.set_stationary_state()

    def set_initial_state(self, dictionary_state):
        for name, state in self.__kinetic_states.items():
            state.update(dictionary_state[name])

    def set_stationary_state(self):
        self.__stationary_state = self.get_current_state()

    def get_stationary_state(self):
        return self.__stationary_state

    def get_graph(self):
        f = Digraph('Synapse', 
                    filename='fsm.gv',
                    node_attr={'color': 'lightblue2', 'style': 'filled'}
                    )

        f.attr(rankdir='LR', size='8,5')
        f.attr('node', shape='doublecircle')

        for _, reaction in self.__reactions.items():
            origin = list(reaction.get_origin().keys())[0]
            destination = list(reaction.get_destination().keys())[0]
            label = reaction.get_rate_reaction().get_name()
            
            if reaction.get_rate_reaction().get_stimulation():
                label = label + "*"

            f.edge(origin, destination, label=label)
        return f
        #f.view()
