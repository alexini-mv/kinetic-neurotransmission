# Dynamics of Neuromuscular Transmission Reproduced by Calcium-Dependent and Reversible Serial Transitions in the Vesicle Fusion Complex

## KiNeuron: Python implementation of the kinetic model of neuromuscular transmission dynamics.

![](https://img.shields.io/static/v1?label=python&message=3.6%20|%203.7%20|%203.8%20|%203.9%20|%203.10&color=informational)
![](https://img.shields.io/static/v1?label=pypi%20package&message=v0.1.0&color=%2334D058)
![](https://img.shields.io/static/v1?label=test&message=passed&color=%2334D058)
[![](https://img.shields.io/static/v1?label=DOI&message=10.3389/fnsyn.2021.785361&color=informational)](https://www.frontiersin.org/articles/10.3389/fnsyn.2021.785361)

KiNeuron is an open-source implementation of our mechanistic kinetic model of neuromuscular transmission based on sequential maturation transitions in the molecular fusion complex.

KiNeuron is:

- **Simple** -- It is possible to simulate an alternative kinetic model with a few lines of code. This way, you can focus on the key parts of the problem that really matter.
- **Flexible** -- It is possible to customize the kinetic model by adjusting the number of transition states, the kinetic transitions between states, as well as the rate constants. Further, KiNeuron allows the addition of a stimulation protocol.

---

- **Source Code**: <a href="https://github.com/alexini-mv/kinetic-neurotransmission" target="_blank">https://github.com/alexini-mv/kinetic-neurotransmission</a>
- **Bug reports**: <a href="https://github.com/alexini-mv/kinetic-neurotransmission/issues" target="_blank">https://github.com/alexini-mv/kinetic-neurotransmission/issues</a>
- **Citing in your work**: https://www.frontiersin.org/articles/10.3389/fnsyn.2021.785361

---

## Requirements

KiNeuron requires:

- python >= 3.6
- graphviz >= 0.19.1
- matplotlib >= 3.3.4
- numpy >= 1.19.5
- pandas >= 1.1.5, <1.3.0

To use the graph display functions of the model, it is necessary to install the Graphviz library as described in follow [documentation](https://graphviz.org/download/).

## Installation

There are two ways to install KiNeuron:

1. Via PyPI repository (recommended):

    - In your local workspace, create a new Python Virtual Environment with [venv](https://docs.python.org/3/library/venv.html) or [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).
    - Install KiNeuron as follow:

    ```console
    $ python -m pip install -U kineuron
    ```

    - All dependencies are downloaded and installed. To verify that it has been installed correctly, you can check the following output:

    ```console
    $ python -c "import kineuron; print(kineuron.__version__)"
    '0.1.0'
    ```

2. Via GitHub:

    - Clone this project [repository](https://github.com/alexini-mv/kinetic-neurotransmission) to your local workspace.
    - Create a new Python Virtual Environment with [venv](https://docs.python.org/3/library/venv.html) or [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).
    - Install the required libraries from the file `requeriments.txt` into your virtual environment as follow:

    ```console
    $ python -m pip install -r requeriments.txt
    ```

You are ready to use KiNeuron.

## Usage Example

### Creating a Model

Create a file `main.py` and import the following classes:

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

tr1 = Transition(name='Transition 1',
                 rate_constant=alpha,
                 origin="Docked",
                 destination="Fusion")
tr2 = Transition(name='Transition 2',
                 rate_constant=beta,
                 origin="Fusion",
                 destination="Docked")
```

Add all objects to the model as follow:

```python
model.add_transition_states([docked, fusion])
model.add_rate_constants([alpha, beta])
model.add_transitions([tr1, tr2])
```

Finally, initialize the model:

```python
model.init()
```

Likewise, a stimulation protocol should be defined (if the experiment expects it) as follows:

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
<img src="https://raw.githubusercontent.com/alexini-mv/kinetic-neurotransmission/main/docs/_static/protocol.png" alt="Stimulation protocol">
</p>

### Model Information (Optional)

General model information can be obtained as follows:

```python
model.get_info()
```

and run the file main.py:

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
<img src="https://raw.githubusercontent.com/alexini-mv/kinetic-neurotransmission/main/docs/_static/graph_model.png" alt="Graph Model">
</p>

### Run It

The Solver object that simulates the time evolution of the model must be instantiated. Here, we use an implementation of the [Gillespie Stochastic Algorithm (1977)](https://doi.org/10.1021/j100540a008).

```python
experiment = Solver(model=model, stimulation=protocol)
```

Before initiating the simulation, be sure to obtain the _**resting state**_ of the model, from which all repetitions of the experiment are starting. This is achieved as follows:

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

- 0.1.0
  - Stable version released.
- 0.0.1
  - Work in progress.

## Contributing

- If you are interested in contributing to the project, please follow these guidelines:

  1.  Fork it (https://github.com/alexini-mv/kinetic-neurotransmission).
  2.  Create your feature branch:

  ```console
  $ git checkout -b feature/fooBar
  ```

  3.  Commit your changes:

  ```console
  $ git commit -am 'Add some fooBar'
  ```

  4.  Push to the branch:

  ```console
  $ git push origin feature/fooBar
  ```

  5.  Create a new Pull Request.

- If you want to report a bug, please create a new issue [here](https://github.com/alexini-mv/kinetic-neurotransmission/issues) describing the error as clearly as possible.

## Correspondence

Author: Alejandro Martínez-Valencia <a href="https://github.com/alexini-mv" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="23"></a>
<a href="https://twitter.com/alexinimv" target="_blank"><img src="https://img.icons8.com/fluency/96/000000/twitter-squared.png" width="25"></a> <a href="https://www.linkedin.com/in/amartinezvalencia/" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="22"></a>

Email: al.martinez.valencia@gmail.com

## Citation

If you use our code for your research or scientific publication, we kindly ask you to refer to our work as follows:

- Martínez-Valencia A., Ramírez-Santiago G. and De-Miguel F.F. (2022) _Dynamics of Neuromuscular Transmission Reproduced by Calcium-Dependent and Reversible Serial Transitions in the Vesicle Fusion Complex_. Front. Synaptic Neurosci. 13:785361. DOI: [10.3389/fnsyn.2021.785361](https://www.frontiersin.org/articles/10.3389/fnsyn.2021.785361)

## License

Distributed under the GNU General Public License. See `LICENSE` for more information.

## Interesting Links

- Perkel, Jeffrey M. (2022) _How to fix your scientific coding errors_. Nature 602, 172-173. DOI: [10.1038/d41586-022-00217-0](https://doi.org/10.1038/d41586-022-00217-0).
- **Pylint**, a tool that checks for errors in Python code. [Tutorials and documentation](https://pylint.pycqa.org/en/latest/index.html).
- **Autopep8**, a package automatically formats Python code to conform to the PEP 8 style guide. [Documentation](https://github.com/hhatto/autopep8).
