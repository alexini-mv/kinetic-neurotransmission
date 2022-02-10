# Dynamics of Neuromuscular Transmission Reproduced by Calcium-Dependent and Reversible Serial Transitions in the Vesicle Fusion Complex

## KiNeuron: Python implementation of the kinetic model of neuromuscular transmission dynamics.

![](https://img.shields.io/static/v1?label=python&message=3.6|3.7|3.8|3.9|3.10&color=informational)
![](https://img.shields.io/static/v1?label=pypi%20package&message=v0.0.1&color=%2334D058)
[![](https://img.shields.io/static/v1?label=DOI&message=10.3389/fnsyn.2021.785361&color=informational)](
https://www.frontiersin.org/articles/10.3389/fnsyn.2021.785361)

KiNeuron is an open source implementation of our mechanistic kinetic model of neuromuscular transmission based on sequential maturation transitions in the molecular fusion complex.

KiNeuron is:

- **Simple** -- It is possible to simulate a new kinetic model with a few lines of code  to free you to focus on the parts of the problem that really matter.
- **Flexible** -- It is possible to customize the kinetic model by changing the number of transition states, the kinetic transitions between states, as well as the rate constants. In addition, KiNeuron allows the addition of stimulation.

---

- **Source Code**: <a href="https://github.com/alexini-mv/kinetic-neurotransmission" target="_blank">https://github.com/alexini-mv/kinetic-neurotransmission</a>
- **Bug reports**: <a href="https://github.com/alexini-mv/kinetic-neurotransmission/issues" target="_blank">https://github.com/alexini-mv/kinetic-neurotransmission/issues</a>
- **Citing in your work**: https://www.frontiersin.org/articles/10.3389/fnsyn.2021.785361
---

## Requirements

KiNeuron requires:

- python (>= 3.6)
- graphviz (>= 0.16)
- matplotlib (>= 3.3.4)
- numpy (>= 1.20.1)
- pandas (>= 1.2.3)

To use the graph display functions of the model, it is necessary to install the Graphviz library as described in the follow [documentation](https://graphviz.org/download/).


## Installation

- Clone this project [repository](https://github.com/alexini-mv/kinetic-neurotransmission) to your local workspace. 
- Create a new Python Virtual Environment with either [venv](https://docs.python.org/3/library/venv.html) or [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).
- Install the required libraries from the file `requeriments.txt` into your virtual environment. 

You are ready to use our package.

## Usage Example

### Creating a Model

Create a file `main.py` importing the following classes:

```python
from kineuron import (KineticModel, RateConstant, Solver, Stimulation,
                      Transition, TransitionState)
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

Likewise, a stimulation protocol should be defined (if the experiment requires it) as follows:

```python
protocol = Stimulation(
     conditional_stimuli=5,
     period=0.03,
     time_start_stimulation=0.1,
     tau_stimulus=0.0013,
     time_wait_test=0.2,
     intensity_stimulus=100.0,
     type_stimulus='exponential_decay', 
     name="Custom Stimulation Protocol")
```

The following lines show the time profile of the stimulation protocol:

```python
import numpy as np

t = np.arange(0, 0.5, 0.0001)
protocol.plot(t)
``` 

<p align="center">
<img src="https://raw.githubusercontent.com/alexini-mv/kinetic-neurotransmission/develop/docs/_static/protocol.png" alt="Stimulation protocol">
</p>


### Model Information (Optional)

General model information can be obtained as follows:
```python
model.get_info()
```
and running the file main.py:


```console
$ python main.py 

==============  MODEL INFORMATION  ===============
MODEL NAME:                   my-model
TOTAL VESICLES:               100

TRANSITION STATES             VESICLES
Docked:                       100
Fusion:                       0
--------------------------------------------------
NAME TRANSITION:              Transition 1
RATE CONSTANT NAME:           α
RATE CONSTANT VALUE:          0.3 s⁻¹
CALCIUM-DEPENDENT:            True
ORIGIN:                       Docked
DESTINATION:                  Fusion
--------------------------------------------------
NAME TRANSITION:              Transition 2
RATE CONSTANT NAME:           β
RATE CONSTANT VALUE:          15 s⁻¹
CALCIUM-DEPENDENT:            False
ORIGIN:                       Fusion
DESTINATION:                  Docked
==================================================
```

The following lines allow you to visualize the graph of the model:

```python
graph = model.get_graph()
graph.view()
```

<p align="center">
<img src="https://raw.githubusercontent.com/alexini-mv/kinetic-neurotransmission/develop/docs/_static/graph_model.png" alt="Graph Model">
</p>


### Run It

The Solver object that simulates the time evolution of the model must be instantiated. Here we use a implementation of the [Gillespie Stochastic Algorithm (1977)](https://doi.org/10.1021/j100540a008).

```python
experiment = Solver(model=model, stimulation=protocol)
```

Before starting the simulation, be sure to find the _**resting state**_ of the model, from which all experiments will start. This is accomplished as follows:

```python
experiment.resting_state()
```

With the following lines the experiment is run. The results can be obtained and saved in a `.csv` file for further analysis.

```python
experiment.run(repeat=1)
results = experiment.get_results(mean=True)
results.to_csv("results.csv", index=True)
```

Finally, the `main.py` file is executed to perform the complete simulation:
```console
$ python main.py
```

## Release History

* 0.0.1
    * Work in progress.

## Contributing
- If you are interested in contributing to the project, please follow these guidelines:

     1. Fork it (https://github.com/alexini-mv/kinetic-neurotransmission)
     2. Create your feature branch 
     ```console
     $ git checkout -b feature/fooBar
     ```
     3. Commit your changes 
     ```console
     $ git commit -am 'Add some fooBar'
     ```
     4. Push to the branch 
     ```console
     $ git push origin feature/fooBar
     ```
     5. Create a new Pull Request

- If you want to report a bug, please create a new issue [here](https://github.com/alexini-mv/kinetic-neurotransmission/issues) describing the error as clearly as possible.

## Correspondence

Author: Alejandro Martínez-Valencia <a href="https://github.com/alexini-mv" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="23"></a>
<a href="https://twitter.com/alexinimv" target="_blank"><img src="https://img.icons8.com/fluency/96/000000/twitter-squared.png" width="25"></a> <a href="https://www.linkedin.com/in/amartinezvalencia/" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="22"></a>

Email: al.martinez.valencia@gmail.com

## Citation
If you use our code for your research or scientific publication, we kindly ask you to cite our work as follows:

* Martínez-Valencia A., Ramírez-Santiago G. and De-Miguel F.F. (2022) _Dynamics of Neuromuscular Transmission Reproduced by Calcium-Dependent and Reversible Serial Transitions in the Vesicle Fusion Complex_. Front. Synaptic Neurosci. 13:785361. DOI: [10.3389/fnsyn.2021.785361](https://www.frontiersin.org/articles/10.3389/fnsyn.2021.785361)


## License

Distributed under the GNU General Public License. See ``LICENSE`` for more information.

## Interesting Links

- Perkel, Jeffrey M. (2022) _How to fix your scientific coding errors_. Nature 602, 172-173. DOI: [10.1038/d41586-022-00217-0](https://doi.org/10.1038/d41586-022-00217-0).
- **Pylint**, a tool that checks for errors in Python code. [Tutorials and documentation](https://pylint.pycqa.org/en/latest/index.html).
- **Autopep8**, a package automatically formats Python code to conform to the PEP 8 style guide. [Documentation](https://github.com/hhatto/autopep8).
