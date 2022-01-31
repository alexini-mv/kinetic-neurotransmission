# Dynamics of Neuromuscular Transmission Reproduced by Calcium-Dependent and Reversible Serial Transitions in the Vesicle Fusion Complex

## Python implementation of the kinetic model of neuromuscular transmission dynamics.


## Requirements

- Python 3.6+
- graphviz
- matplotlib
- numpy
- pandas

To use the graph display functions of the model, it is necessary to install the Graphviz library as described in the follow [documentation](https://graphviz.org/download/).


## Installation

Clone the project [repository](https://github.com/alexini-mv/kinetic-neurotransmission) to your local workspace. Create a new Python Virtual Environment with either [venv](https://docs.python.org/3/library/venv.html) or [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html). Install the required libraries from the file `requeriments.txt` into your virtual environment. You are ready to use our package.

## Example

### Creating a model

Create a file `main.py` importing the following classes:

```python
from kineuron import KineticModel, TransitionState, Transition
from kineuron import RateConstant, Stimulation, Solver
``` 

After, instance the model objects as follows:

```python
model = KineticModel(name='my-model', vesicles=100)

docked = TransitionState(name='Docked')
fusion = TransitionState(name='Fusion')

alpha = RateConstant(name="α", value=0.3, calcium_dependent=True)
beta = RateConstant(name="β", value=15)

tr1 = Transition(name='Transition 1', rate_constant=alpha, origin={"Docked": 1}, destination={"Fusion": 1})
tr2 = Transition(name='Transition 2', rate_constant=beta, origin={"Fusion": 1}, destination={"Docked": 1})
```

Add all objects to the model as follows:

```python
model.add_transition_states([docked, fusion])
model.add_rate_constants([alpha, beta])
model.add_transitions([tr1, tr2])
```

Finally initialize the model:
```python
model.init()
```

Tambien, define un protocolo de estimulación costume como sigue:

```python
protocol = Stimulation(
     conditional_stimuli=5,
     period=0.03,
     time_start_stimulation=0.1,
     tau_stimulus=0.0013,
     time_wait_test=0.2,
     intensity_stimulus=100.0,
     type_stimulus='exponential_decay', 
     name="Costum Stimulation Protocol")
```

Con las siguientes linea puedes ver visualizar el perfil temporal del protocolo de estimulación:
```python
import numpy as np

t = np.arange(0, 0.5, 0.0001)
protocol.plot(t)
``` 
![](protocol.png)

### Model information (optional)

General model information can be obtained as follows:
```python
model.get_info()
```
and running the file main.py:


```console
$ python main.py 

================ MODEL INFORMATION ================
MODEL NAME:	my-model
TOTAL VESICLES:	100

TRANSITION STATES - VESICLES
Docked	:	100
Fusion	:	0
----------------------------------------------------
NAME:		Transition 1
RATE CONSTANT NAME:	α
RATE CONSTANT VALUE:	0.3 s⁻¹
CALCIUM-DEPENDENT:	True
ORIGIN:		{'Docked': 1}
DESTINATION:	{'Fusion': 1}
----------------------------------------------------
NAME:		Transition 2
RATE CONSTANT NAME:	β
RATE CONSTANT VALUE:	15 s⁻¹
CALCIUM-DEPENDENT:	False
ORIGIN:		{'Fusion': 1}
DESTINATION:	{'Docked': 1}
====================================================
```


The following lines allow you to visualize the graph of the model:

```python
graph = model.get_graph()
graph.view()
```
![](graph_model.jpg)

### Run it
Se instancia el Solver que simulará la evolución temporal del modelo, usando el Algoritmo Estocastico de Gillespie (1976).

```python
experiment = Solver(model=model, stimulation=protocol)
```

Después, se debe buscar el `resting state` del modelo a partir del cual se comenzaran a hacer los experimentos:

```python
experiment.resting_state()
```

Con las siguientes lineas se ejecuta el experimento, se pueden obtener los resultados y se guardan en un archivo `.csv` para el análisis posterior.

```python
experiment.run(repeat=1)
results = experiment.get_results(mean=True)
results.to_csv("results.csv", index=True)
```

Finalmente, se ejecuta el archivo `main.py` para realizar la simulación:
```console
$ python main.py
```

## Reference
Si usas nuestro código para tu investigación, te pedimos amablemente citar nuestro trabajo como sigue:

Martínez-Valencia. A, Ramírez-Santiago. G, De-Miguel, F. F. (2022). Frontiers in Synaptic Neuroscience. URL: https://www.frontiersin.org/articles/10.3389/fnsyn.2021.785361
