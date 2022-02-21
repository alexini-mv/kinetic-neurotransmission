import matplotlib.pyplot as plt
import numpy as np

from kineuron import (KineticModel, RateConstant, Solver, Stimulation,
                      Transition, TransitionState)

model = KineticModel(name='my-model', vesicles=100)

docked = TransitionState(name='Docked')
fusion = TransitionState(name='Fusion')

alpha = RateConstant(name="α", value=0.3, calcium_dependent=True)
beta = RateConstant(name="β", value=15)

tr1 = Transition(name='Transition 1', rate_constant=alpha,
                 origin="Docked", destination="Fusion")
tr2 = Transition(name='Transition 2', rate_constant=beta,
                 origin="Fusion", destination="Docked")

model.add_transition_states([docked, fusion])
model.add_rate_constants([alpha, beta])
model.add_transitions([tr1, tr2])

model.init()
model.get_info()
# graph = model.get_graph()
# graph.view()


protocol = Stimulation(
    conditional_stimuli=5,
    period=0.03,
    time_start_stimulation=0.1,
    tau_stimulus=0.0013,
    time_wait_test=0.2,
    intensity_stimulus=1000.0,
    type_stimulus='exponential_decay',
    name="Custom Stimulation Protocol")

# t = np.arange(0, 0.5, 0.0001)
# protocol.plot(t)

experiment = Solver(model=model, stimulation=protocol)
experiment.resting_state()

experiment.run(repeat=500)
# results = experiment.get_results(mean=True)
# results.plot()
# plt.show()

# results.to_csv("results.csv", index=True)
