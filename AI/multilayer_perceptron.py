'''
Created on 19-03-2012

@author: WZ
'''
from neural.activation_functions import *
import random
import math


class WeightInitializeMethod:
	"""Enumeration type for weight initialization method."""
	RANDOM_INIT = "RANDOM_INIT"
	ZERO_INIT = "ZERO_INIT"

class MultilayerPerceptron(object):
	'''
	Simple multilayer perceptron model (feedforward network architecture).
	A multilayer perceptron is a feedforward artificial neural network model that maps sets of input data onto a set of appropriate output. 
	An MLP consists of multiple layers of nodes in a directed graph, with each layer fully connected to the next one. 
	Except for the input nodes, each node is a neuron (or processing element) with a nonlinear activation function. 
	'''

	def __init__(self, inputs_n, outputs_n):
		'''
		Multilayer perceptron constructor. Set input and output layers' lengths.
		@param inputs_n: indicating length of the input layer
		@param outputs_n: indicating length of the output layer
		'''
		self.weight_matrix = None
		self.activation_matrix = [[0] * inputs_n] + [[0] * outputs_n]
		self.ActivationFunction = LogisticActivationFunction
		self.ActivationFunctionDeriv = LogisticDerivActivationFunction
		self.weight_magnitude_limit = 0.0
		self.weight_initial_random_magnitude = 0.5
		
	
	
		
	def InitializeWeights(self, method_s=WeightInitializeMethod.RANDOM_INIT):
		"""
		Initialize weight vector so that further computation can be done.
		Several weight initialization methods can be choosed. Default is random initialization with range <-0.5;0.5>.
		Warning! No calculations can be done without executing this method first!
		@param method_s: method chosen for weight initialization
		"""
		n = len(self.activation_matrix)
		self.weight_matrix = [None] * (n - 1)
		
		if method_s == WeightInitializeMethod.RANDOM_INIT:
			for i in range(1, n):  # For each layer ( minus input layer ).
				self.weight_matrix[i - 1] = [None] * len(self.activation_matrix[i]) 
				for j in range (0, len(self.activation_matrix[i])):  # For each neuron.
					self.weight_matrix[i - 1][j] = [1.0] * (len(self.activation_matrix[i - 1]) + 1)  # Previous layer size + bias
					for k in range(0, len(self.activation_matrix[i - 1])):  # For each connection with previous layer.
																									# Generate random number from range <-x; x> , best is <-0.5; 0.5>
						self.weight_matrix[i - 1][j][k] = random.uniform(-self.weight_initial_random_magnitude, self.weight_initial_random_magnitude)


	
	def SetHiddenLayers(self, layer_map_l):
		"""
		Method responsible for generating hidden layers for the network.
		@param layer_map_l: list representing number of neurons in each hidden layer
		"""
		
		del self.activation_matrix[1:-1]
		for layer_size in layer_map_l:
			self.activation_matrix[-1:-1] = [[0.0] * layer_size]
			
	
	def ComputeOutput(self, input_layer_l):
		"""
		Method performing calculations for target input layer and setting new activation level for every neuron.
		@param input_layer: target input layer
		@return: output layer
		"""
		if self.weight_matrix == None or len(self.weight_matrix) == 0:
			raise Exception("Weight matrix was not initialized.")
			
		if len(input_layer_l) != len(self.activation_matrix[0]):
			raise Exception("Input layer has wrong size.")
		
		for i in range(1, len(self.activation_matrix)):  # Each layer, except first
			for j in range(0, len(self.activation_matrix[i])):  # Each neuron
				self.activation_matrix[i][j] = self.weight_matrix[i - 1][j][-1];  # Set bias
				for k in range(0, len(self.activation_matrix[i - 1])):  # Each previous connection
					self.activation_matrix[i][j] += self.activation_matrix[i - 1][k] * self.weight_matrix[i - 1][j][k];
				self.activation_matrix[i][j] = self.ActivationFunction(self.activation_matrix[i][j]);
				
		return self.activation_matrix[-1]
	
	def Execute(self, input_layer_l):
		return self.ComputeOutput(input_layer_l)
	
	def GetNetworkLayerMap(self):
		"""
		Generates vector, where each row indicate layer ( including input and output layers ) and value indicate number of neurons present in that layer.
		@return: list with network map.
		"""
		return [len(x) for x in self.activation_matrix]
	
	def SetWeightMagnitudeLimit(self, limit=5.0):
		"""
		Set limitation for each weight's magnitude.
		There is rarely any need for extremely large weights thus we can set limit for weights' magnitude.
		The absolute value of each weight should not be allowed to exceed this limit.
		A limit of five is sufficiently large to permit wide variation and small enough to let gradient techniques pull it in later if necessary.
		@param limit:  Sets weight limit.
		"""
		self.weight_magnitude_limit = limit
		
		for layer in self.weight_matrix:
			for neuron in layer:
				for weight in neuron:
					if weight > limit:
						weight = limit
	
	def SetWeightInitRandomMagnitude(self, magnitude=0.5):
		"""
		Set maximal magnitude value in case of random initial weight generation.
		@param magnitude: sets weight maximal magnitude.
		"""
		self.weight_initial_random_magnitude = abs(magnitude)
	
	def SetBiasForAll(self, value=1.0):
		"""
		Set bias value for every neuron in the network.
		@param value: target bias value.
		"""
		for layer in self.weight_matrix:
			for neuron in layer:
				neuron[-1] = value  # Bias value
				
	@property
	def input(self):
		"""Input layer"""
		return self.activation_matrix[0]
	
#	@input.setter
#	def input(self, input_layer_l):
#		"""Input layer"""
#		self.activation_matrix[0] = input_layer_l
	
	@property
	def output(self):
		"""Output layer"""
		return self.activation_matrix[-1]
	
#	def __call__(self, layer_id, neuron_id):
#		if self.activationMatrix == None:
#			raise Exception("Activation matrix was not initialized yet.")
#		else:
#			return self.activationMatrix[layer_id][neuron_id]
#	
#	def __call__(self, layer_id, neuron_id, connection_id):
#		if self.weightMatrix == None:
#			raise Exception("Weight matrix was not initialized yet.")
#		else:
#			return self.activationMatrix[layer_id][neuron_id][connection_id]
	
if __name__ == "__main__":
	lol = MultilayerPerceptron(2, 2)
	lol.SetHiddenLayers([3])
	lol.SetWeightInitRandomMagnitude(0.5)
	lol.InitializeWeights()
	lol.SetBiasForAll(10)
	lol.ComputeOutput([1, 0])
	lol.SetWeightMagnitudeLimit(0.1)
	
	# Show
	print(lol.GetNetworkLayerMap())
	print(lol.activation_matrix)
	print(lol.weight_matrix)
	print(lol.input, lol.output)
	
