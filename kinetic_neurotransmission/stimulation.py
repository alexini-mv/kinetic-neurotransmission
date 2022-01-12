import math

import matplotlib.pyplot as plt 
from numpy import vectorize

from .neuromuscular import Synapse

class Stimulation(Synapse):
	"""Definimos el calcium-dependence estimulación que se utilizará dentro 
	de la simulación del modelo.

	Methods
	-------
	stimuli(t : float)
		Regresa el valor de la función de estimulación en el tiempo t.
	plot(t : numpy.array)
		Gráfica el perfil de estimulación sobre un rango de tiempo definido
		por el numpy.array.
	get_info()
		Imprime la información general del protocolo de estimulación: nombre
		del Stimulation object, tipo de estimulación, duración de cada estimulo,
		intensidad del estímulo, periodo de tiempo entre cada estimulo, etc.
	"""

	def __init__(self, time_start_stimulation, conditional_stimuli, period, 
		tau_stimulus, intensity_stimulus, time_wait_test,  
		type_stimulus='exponential_decay', name="Stimulation Protocol"):
		"""Se inicializa el objeto Stimulation.

		Parameters
		----------
		time_start_stimulation : float
			Tiempo en el cual inicia la estimulación dentro de la evolución 
			temporal del Modelo.
		conditional_stimuli : int
			Numero de estímulos condicionales.
		period : float
			Tiempo de espera entre cada estimulo condicional. En caso de que el
			número de estimulos condicionales sea uno, el periodo se omite.
		tau_stimulus: float
			Constante de tiempo que caracteriza la duración de cada estimulo.
		intensity_stimulus : float
			Intensidad cada estimulo definido en unidades arbitrarias
		time_wait_test : float
			Intervalo de tiempo de espera entre el último estimulo condicional
			y el estimulo de prueba
		type_stimulus : str, opcional
			Tipo del perfil de cada estimulo individual. Por default el valor
			del parametro es 'exponential_delay' que corresponde a un estimulo 
			con subida instantanea seguido de un decaimiento exponencial.
		name : str, optional
			Nombre del protocolo de estimulación.
		"""

		super().__init__(name)

		assert type_stimulus == 'exponential_decay', \
			f"The object '{self.__class__.__name__}' no accept '{type_stimulus}' argument of type_stimuli."
		
		epsilon = 0.005
		self.__conditional_stimuli = conditional_stimuli
		self.__period = period
		self.__time_start_stimulation = time_start_stimulation
		self.__tau_stimulus = tau_stimulus
		self.__time_wait_test = time_wait_test
		self.__intensity_stimulus = intensity_stimulus
		self.__type_stimulus = type_stimulus

		self.__time_end_stimulation = time_start_stimulation + (conditional_stimuli 
															   - 1) * period + epsilon

	def get_info(self):
		print("**** Información con los detalles del protocolo de estimulación. ****")
		print(f"Nombre del protocolo de estimulación:\t\t{self.get_name()}")
		print(f"Tipo de estímulo:\t\t\t\t {self.__type_stimulus}")
		print(f"Número de estímulos condicionales:\t\t {self.__conditional_stimuli}")
		print(f"Tiempo de inicio de estimulación:\t\t {self.__time_start_stimulation}")
		print(f"Tiempo de finalización de estimulación:\t\t {self.__time_end_stimulation}")
		print(f"Periodo entre estímulos:\t\t\t {self.__period}")
		print(f"Tau de estimulación:\t\t\t\t {self.__tau_stimulus}")
		print(f"Espera entre el último condicional y test:\t {self.__time_wait_test}")
		print(f"Intensidad del estimulo:\t\t\t {self.__intensity_stimulus}")

	def stimuli(self, t):
		'''Función que modela la estimulación dentro del modelo.

		Parameters
		----------
		t : float
			Variable temporal dentro de la evolución del modelo.

		Return
		------
		float
			El valor del estimulo en el tiempo t.
		'''

		delta_time = t - self.__time_start_stimulation

		time_test = self.__time_start_stimulation + (self.__conditional_stimuli 
														- 1) * self.__period + self.__time_wait_test
														
		if t >= self.__time_start_stimulation and t < self.__time_end_stimulation:
			f = math.exp(-(delta_time % self.__period) / self.__tau_stimulus)
		elif t >= self.__time_end_stimulation and t < time_test:
			f = math.exp(-(delta_time - (self.__conditional_stimuli - 1) * self.__period) / self.__tau_stimulus)
		elif t >= time_test:
			f = math.exp(-(t - time_test) / self.__tau_stimulus)
		else:
			f = 0.0
		
		return self.__intensity_stimulus * f

	def plot(self, t, xlabel="Time", ylabel="Intensity"):
		"""Grafica el perfil del protocolo de estimulación dentro de un 
		intervalo de tiempo.

		Parameters
		----------
		t : numpy.array
			Arreglo con los valores de los puntos en donde se gráficara el 
			protocolo de estimulación.
		xlabel : str, optional
			Nombre de la etiqueta del eje x de la gráfica. Por default 'Time'
		ylabel : str, optional
			Nombre de la etiqueta del eje y de la gráfica. Por default 'Intensity'
		"""
		y = vectorize(self.stimuli)(t)
		plt.plot(t, y)
		plt.title(self.get_name())
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.show()
		
