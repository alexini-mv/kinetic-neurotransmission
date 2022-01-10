#!/usr/bin/python3
import time 

import matplotlib.pyplot as plt

from kinetic_neurotransmission import KineticModel, TransitionState, Transition, RateConstant
from kinetic_neurotransmission import Stimulation, Solver

from parameters import *

model = KineticModel(name='Kinetic Neuromuscular Transmission', vesicles=numero_vesiculas)

docked = TransitionState(name='Docked')
pprimed = TransitionState(name='pPrimed')
primed = TransitionState(name='Primed')
fusion = TransitionState(name='Fusion')

r_alpha = RateConstant(name="α", value=alpha, stimulation=True)
r_beta = RateConstant(name="β", value=beta)
r_rho = RateConstant(name="ρ", value=rho)

tr1 = Transition(name='Transition 1', rate_constant=r_alpha, origin={"Docked": 1}, destination={"pPrimed": 1})
tr2 = Transition(name='Transition 2', rate_constant=r_beta, origin={"pPrimed": 1}, destination={"Docked": 1})
tr3 = Transition(name='Transition 3', rate_constant=r_alpha, origin={"pPrimed": 1}, destination={"Primed": 1})
tr4 = Transition(name='Transition 4', rate_constant=r_beta, origin={"Primed": 1}, destination={"pPrimed": 1})
tr5 = Transition(name='Transition 5', rate_constant=r_alpha, origin={"Primed": 1}, destination={"Fusion": 1})
tr6 = Transition(name='Transition 6', rate_constant=r_rho, origin={"Fusion": 1}, destination={"Docked": 1})

model.add_transition_states([docked, pprimed, primed, fusion])
model.add_transitions([tr1, tr2, tr3, tr4, tr5, tr6])
model.add_rate_constants([r_alpha, r_beta, r_rho])

model.init()

model.get_info()

#graph = model.get_graph()
#graph.view()

# protocol = Stimulation(
#     conditional_stimuli=3,
#     period=0.3,
#     time_start_stimulation=0.1,
#     tau_stimulation=0.001,
#     time_wait_test=0.1,
#     intensity_stimulus=500.0)

# # t = arange(0, 90, 0.1)
# # protocol.plot(t)

# experiment = Solver(model=model, stimulation=protocol)
# start = time.time()
# experiment.resting_state()
# print(time.time()-start)
# experiment.run(repeat=1)

# experiment.get_resting_simulation().plot()
# plt.show()
