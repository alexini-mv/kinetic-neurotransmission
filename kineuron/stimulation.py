import math

import matplotlib.pyplot as plt
import numpy as np

from .neuromuscular import Synapse


class Stimulation(Synapse):
    """The calcium-dependent stimulation to be used in the simulation of the 
    kinetic model is defined.

    Methods
    -------
    stimuli
        Returns the value of the stimulation function at time t.
    plot
        Plots the stimulation profile over a time range defined by 
        a numpy.array.
    get_info
        Prints the general information of the stimulation protocol, i.e. the 
        name of the kineuron.Stimulation object, type of stimulation, duration 
        of each stimulus, intensity of the stimulus, time period between 
        each stimulus, etc.
    """

    def __init__(self, name: str = "Stimulation Protocol",
                 time_start_stimulation: float = None,
                 conditional_stimuli: int = None, period: float = None,
                 tau_stimulus: float = None, intensity_stimulus: float = None,
                 time_wait_test: float = None,
                 type_stimulus: str = 'exponential_decay') -> None:
        """
        Parameters
        ----------
        name : str, optional
            Stimulation protocol name.
        time_start_stimulation : float
            Time at which the stimulation starts within the time evolution of 
            the model simulation.
        conditional_stimuli : int
            Number of conditional stimuli.
        period : float
            Waiting time between each conditional stimulus. In case the 
            number of conditional number of conditional stimuli is one, the 
            period is omitted.
        tau_stimulus: float
            Time constant of the duration of each individual stimulus.
        intensity_stimulus : float
            Intensity each stimulus defined in arbitrary units.
        time_wait_test : float
            Waiting time interval between the last conditional stimulus and 
            the test stimulus.
        type_stimulus : str, opcional
            Profile of each individual stimulus. By default, the parameter 
            value is 'exponential_delay' which corresponds to a stimulus 
            with an instantaneous rise followed by an exponential decay.
        """

        super().__init__(name)

        message = f"The '{self.__class__.__name__}' object does not accept" + \
            f" '{type_stimulus}' as a valid value of 'type_stimulus'."

        assert type_stimulus == 'exponential_decay', message

        epsilon = 0.005
        self.__time_start_stimulation: float = time_start_stimulation
        self.__conditional_stimuli: int = conditional_stimuli
        self.__period: float = period
        self.__tau_stimulus: float = tau_stimulus
        self.__time_wait_test: float = time_wait_test
        self.__intensity_stimulus: float = intensity_stimulus
        self.__type_stimulus: str = type_stimulus
        self.__time_end_stimulation: float = time_start_stimulation + \
            (conditional_stimuli - 1) * period + epsilon

    def __str__(self) -> str:
        """Builds a string with the general information of the stimulation 
        protocol, i.e. name, type of stimulation, number of conditional 
        stimuli, initial stimulation time, stimulation end time, period 
        between conditional stimuli, time constant of duration of each 
        stimulus, waiting time between the last conditional stimulus and the 
        test stimulus, intensity of each stimulus.

        Return
        ------
        str
            General information defined within the Stimulation object.
        """
        width = 65
        left = 35

        msg = [
            "  STIMULATION PROTOCOL OVERVIEW  ".center(width, "="),
            "* Name:".ljust(left) + self.get_name(),
            "* Type of stimulus:".ljust(left) + self.__type_stimulus,
            "* Conditional stimuli:".ljust(left) +
            str(self.__conditional_stimuli),
            "* Start time:".ljust(left) +
            str(self.__time_start_stimulation) + " s",
            "* Conditional stimuli period:".ljust(
                left) + str(self.__period) + " s",
            "* Time constant of the stimuli:".ljust(
                left) + str(self.__tau_stimulus) + " s",
            "* Waiting time between last",
            "  conditional and test stimuli:".ljust(
                    left) + str(self.__time_wait_test) + " s",
            "* Stimulus intensity:".ljust(left) +
            str(self.__intensity_stimulus),
            "".center(width, "=")
        ]
        return "\n".join(msg)

    def get_info(self) -> None:
        """Returns the general information of the stimulation protocol, i.e. 
        name, type of stimulation, number of conditional stimuli, initial 
        stimulation time, stimulation end time, period between conditional 
        stimuli, time constant of duration of each stimulus, waiting time 
        between the last conditional stimulus and the test stimulus, intensity 
        of each stimulus.

        Return
        ------
            General information defined within the Stimulation object.
        """
        print(self.__str__())

    def stimuli(self, t: float) -> float:
        '''Function that models the stimulation protocol.

        Parameters
        ----------
        t : float
            Time variable within the model simulation.

        Return
        ------
        float
            The stimulus value at time t.
        '''

        delta_time = t - self.__time_start_stimulation

        time_test = self.__time_start_stimulation + (self.__conditional_stimuli
                                                     - 1) * self.__period + self.__time_wait_test

        if t >= self.__time_start_stimulation and t < self.__time_end_stimulation:
            f = math.exp(-(delta_time % self.__period) / self.__tau_stimulus)
        elif t >= self.__time_end_stimulation and t < time_test:
            f = math.exp(-(delta_time - (self.__conditional_stimuli - 1)
                         * self.__period) / self.__tau_stimulus)
        elif t >= time_test:
            f = math.exp(-(t - time_test) / self.__tau_stimulus)
        else:
            f = 0.0

        return self.__intensity_stimulus * f

    def plot(self, t: float, xlabel: str = "Time",
             ylabel: str = "Intensity") -> None:
        """Plots the profile of the stimulation protocol over a range of time.

        Parameters
        ----------
        t : numpy.array
            Array of values where the stimulation protocol profile is plotted.
        xlabel : str, optional
            Name of the x-axis label of the graph. Default 'Time'.
        ylabel : str, optional
            Name of the y-axis label of the graph. Default 'Intensity'.
        """
        y = np.vectorize(self.stimuli)(t)
        plt.plot(t, y)
        plt.title(self.get_name())
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()
