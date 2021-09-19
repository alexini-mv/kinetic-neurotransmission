#!/usr/bin/python3
import time 

import matplotlib.pyplot as plt

from presinaptic import PresinapticNeuron, KineticState, Reaction, RateReaction
from presinaptic import StimulationProtocol, Solver

from parameters import *

sinapsis = PresinapticNeuron(name='Presinapsis', vesicles=numero_vesiculas)

docked = KineticState(name='Docked')
pprimed = KineticState(name='pPrimed')
primed = KineticState(name='Primed')
fusion = KineticState(name='Fusion')

r_alpha = RateReaction(name="α", rate=alpha, stimulation=True)
r_beta = RateReaction(name="β", rate=beta)
r_rho = RateReaction(name="ρ", rate=rho)

r1 = Reaction(name='r1', rate=r_alpha, origin={"Docked": 1}, destination={"pPrimed": 1})
r2 = Reaction(name='r2', rate=r_beta, origin={"pPrimed": 1}, destination={"Docked": 1})
r3 = Reaction(name='r3', rate=r_alpha, origin={"pPrimed": 1}, destination={"Primed": 1})
r4 = Reaction(name='r4', rate=r_beta, origin={"Primed": 1}, destination={"pPrimed": 1})
r5 = Reaction(name='r5', rate=r_alpha, origin={"Primed": 1}, destination={"Fusion": 1})
r6 = Reaction(name='r6', rate=r_rho, origin={"Fusion": 1}, destination={"Docked": 1})

sinapsis.add_kinetic_states([docked, pprimed, primed, fusion])
sinapsis.add_reactions([r1, r2, r3, r4, r5, r6])
sinapsis.add_rate_reactions([r_alpha, r_beta, r_rho])

sinapsis.init()

#sinapsis.get_info()

graph = sinapsis.get_graph()
graph.view()

# protocol = StimulationProtocol(
#     conditional_stimulis=3,
#     period=0.3,
#     time_start_stimulation=0.1,
#     tau_stimulation=0.001,
#     time_wait_test=0.1,
#     intensity_stimuli=500.0)

# # t = arange(0, 90, 0.1)
# # protocol.plot(t)

# experiment = Solver(synapse=sinapsis, protocol=protocol)
# start = time.time()
# experiment.stationary_state()
# print(time.time()-start)
# experiment.run(repeat=1)

# experiment.get_stationary_simulation().plot()
# plt.show()
