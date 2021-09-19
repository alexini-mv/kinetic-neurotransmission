import math

import matplotlib.pyplot as plt 
from numpy import vectorize

from .synapse import Synapse

class StimulationProtocol(Synapse):
	"""Definimos el protocolo de estimulación que se utilizará para cambiar
	los valores de las constantes de reacción definidas en el objeto RateReaction

	Methods
	-------
	get_info 
		Imprime la información general del protocolo de estimulación, tal como
		el tipo de estimulación, número de estimulos, duración de cada estimulo,
		intensidad del estímulo, etc.
	stimuli(t : float)
		Regresa el valor del estímulo en el tiempo t
	plot(t : numpy.array)
		Gráfica el perfil de estimulación sobre un rango de tiempo definido
		por el arreglo t
	"""

	def __init__(self, time_start_stimulation, conditional_stimulis, period, 
		tau_stimulation, intensity_stimuli, time_wait_test,  
		type_stimuli='exponential_decay', name="Stimulation Protocol"):
		"""Se inicializa el objeto StimulationProtocol

		Parameters
		----------
		time_start_stimulation : float
			Tiempo en el cual inicia la estimulación dentro de la simulación
		conditional_stimulis : int
			Numero de estimulos condicionales
		period : float
			Tiempo de espera entre cada estimulo condicional. En caso de que el
			número de estimulos condicionales sea uno, el periodo se omite
		tau_stimulation : float
			Constante de tiempo que caracteriza la duración del estimulo
		intensity_stimuli : float
			Intensidad máxima de cada estimulo definido en unidades arbitrarias
		time_wait_test : float
			Intervalo de tiempo de espera entre el último estimulo condicional
			y el estimulo de prueba
		type_stimuli : str, opcional
			Tipo del perfil de cada estimulo individual. Por default el valor
			del parametro es 'exponential_delay' que corresponde a un estimulo 
			con subida instantanea a la intensidad máxima, seguida de un 
			decaimiento exponencial
		name : str, optional
			Nombre del protocolo de estimulación. Por default su valor es
			'Stimulation Protocol'
		"""

		super().__init__(name)

		assert type_stimuli == 'exponential_decay', \
			f"The object '{self.__class__.__name__}' no accept '{type_stimuli}' argument of type_stimuli."
		
		epsilon = 0.005
		self.__conditional_stimulis = conditional_stimulis
		self.__period = period
		self.__time_start_stimulation = time_start_stimulation
		self.__tau_stimulation = tau_stimulation
		self.__time_wait_test = time_wait_test
		self.__intensity_stimuli = intensity_stimuli
		self.__type_stimuli = type_stimuli

		self.__time_end_stimulation = time_start_stimulation + (conditional_stimulis 
																		- 1) * period + epsilon

	def get_info(self):
		print("**** Información con los detalles del protocolo de estimulación. ****")
		print(f"Nombre del protocolo de estimulación:\t\t{self.get_name()}")
		print(f"Tipo de estímulo:\t\t\t\t {self.__type_stimuli}")
		print(f"Número de estímulos condicionales:\t\t {self.__conditional_stimulis}")
		print(f"Tiempo de inicio de estimulación:\t\t {self.__time_start_stimulation}")
		print(f"Tiempo de finalización de estimulación:\t\t {self.__time_end_stimulation}")
		print(f"Period entre estímulos:\t\t\t {self.__period}")
		print(f"Tau de estimulación:\t\t\t\t {self.__tau_stimulation}")
		print(f"Espera entre el último condicional y test:\t {self.__time_wait_test}")
		print(f"Intensidad del estimulo:\t\t\t {self.__intensity_stimuli}")

	def stimuli(self, t):
		'''
		Función que modela el protocolo de estimulación externa de la sinapsis neuromuscular.
		En este modelo, se utiliza un perfil de estímulo con caida exponencial.
		'''

		delta_time = t - self.__time_start_stimulation

		time_test = self.__time_start_stimulation + (self.__conditional_stimulis 
														- 1) * self.__period + self.__time_wait_test
														
		if t >= self.__time_start_stimulation and t < self.__time_end_stimulation:
			f = math.exp(-(delta_time % self.__period) / self.__tau_stimulation)
		elif t >= self.__time_end_stimulation and t < time_test:
			f = math.exp(-(delta_time - (self.__conditional_stimulis - 1) * self.__period) / self.__tau_stimulation)
		elif t >= time_test:
			f = math.exp(-(t - time_test) / self.__tau_stimulation)
		else:
			f = 0.0
		
		return self.__intensity_stimuli * f

	def plot(self, t, xlabel="Time", ylabel="Intensity"):
		"""Grafica el protocolo de estimulación dentro de un intervalo de tiempo
		Parameters
		----------
		t : numpy.array
			Arreglo con los valores de los puntos en donde se gráficara el 
			protocolo de estimulación
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
		
