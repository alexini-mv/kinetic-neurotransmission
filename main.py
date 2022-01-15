#!/usr/bin/python3
import time 

from numpy import arange
import matplotlib.pyplot as plt


from kinetic_neurotransmission import KineticModel, TransitionState, Transition, RateConstant
from kinetic_neurotransmission import Stimulation, Solver

# Define simulation parameters

alpha = 1.43
lamda = 100
beta = alpha * lamda
rho = 1.0
vesicles = 10000

# Instantiate the model objects

model = KineticModel(name='Kinetic Neuromuscular Transmission', vesicles=vesicles)

docked = TransitionState(name='Docked')
pprimed = TransitionState(name='pPrimed')
primed = TransitionState(name='Primed')
fusion = TransitionState(name='Fusion')

r_alpha = RateConstant(name="α", value=alpha, calcium_dependent=True)
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

protocol = Stimulation(
     conditional_stimuli=3,
     period=0.03,
     time_start_stimulation=0.1,
     tau_stimulus=0.0013,
     time_wait_test=0.45,
     intensity_stimulus=500.0)

# t = arange(0, 1.0, 0.0001)
# protocol.plot(t)

# We look for the resting state of the model.

experiment = Solver(model=model, stimulation=protocol)
experiment.resting_state(time_end=30.0)

print("Resting State of Model")
print(model.get_resting_state())
print("")
# experiment.get_resting_simulation().plot()
# plt.show()

# Run the stochastic simulation.

print("Running the experiment:")

experiment.run(repeat=1)
resultados = experiment.get_results(mean=True)
resultados.plot()
plt.show()

