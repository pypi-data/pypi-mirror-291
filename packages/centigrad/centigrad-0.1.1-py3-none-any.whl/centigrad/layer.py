from .variable import Variable
import numpy as np

class Layer:
    def __init__(self, 
                 input_dim, 
                 n_neurons, 
                 activation = "sigmoid",
                 initial_weights=None,
                 initial_biases=None):
        """
        Initializes a layer in a neural network where the weights and biases are Variable objects
        with automatic differentiation capabilities.
        
        Parameters:
        -----------
        input_dim : int
            The number of input features to the layer.
        n_neurons : int
            The number of neurons in the layer.
        activation : str, optional
            The activation function of the neuron (default is "sigmoid").
        initial_weights : np.ndarray, optional
            The initial weights for the neurons. If None, weights are initialized randomly.
        initial_biases : np.ndarray, optional
            The initial biases for the neurons. If None, biases are initialized randomly.
        """
        self.input_dim = input_dim
        self.n_neurons = n_neurons
        self.activation = activation

        # Initial weights setting
        if initial_weights is not None:
            self.weights = initial_weights
        else:
            self.weights = np.random.normal(loc=0, scale=1, size=(input_dim, n_neurons))
        # The weights are converted to Variable objects
        self.weights = np.vectorize(Variable)(self.weights)

        # Initial biases setting
        if initial_biases is not None:
            self.biases = initial_biases
        else:
            self.biases = np.random.normal(loc=0, scale=1, size = (n_neurons, 1))
        # The biases are converted to Variable objects
        self.biases = np.vectorize(Variable)(self.biases)

    def __repr__(self):
        """
        Returns a string representation of the Layer object, showing the number of neurons and the activation function.
        
        Returns:
        --------
        str
            A string representation of the layer.
        """
        return f"Layer(neurons={self.n_neurons}, activation = {self.activation})"
    
    def forward(self, input_data):
        """
        Performs the forward pass for the layer by computing the weighted sum and applying the activation function.
        
        Parameters:
        -----------
        input_data : np.ndarray
            The input data to the layer, usually the output from the previous layer or the X matrix if it is the
            first layer
        
        Returns:
        --------
        np.ndarray
            The output of the layer after applying the linear combination and activation function.
        """
        # To guarantee that if the forward methos is called multiple times, the number of parents
        # do not grow but stay the same, the weights are replaced by its value itself
        self.weights = self.weights + 0
        self.biases = self.biases + 0
        
        # The weighted sum is the calculated
        linear_combination = np.matmul(self.weights.T, input_data) + self.biases

        # Then the activation function is calculated for each variable
        # This is currently done with loops (not most efficient solution)
        # TO DO: improve efficiency with vectorization
        iteration_indexes = np.ndindex(linear_combination.shape[0], 
                                        linear_combination.shape[1])
        for entry in iteration_indexes:
            activation = getattr(linear_combination[entry], self.activation)
            linear_combination[entry] = activation()
        return linear_combination
    
    def backward(self):
        """
        Computes the gradient of the loss with respect to the weights and biases of the layer (backward pass).
        
        Returns:
        --------
        tuple of np.ndarray
            The gradients with respect to the weights and biases, respectively.
        """
        gradient_method = getattr(Variable, "grad")
        return np.vectorize(gradient_method)(self.weights), np.vectorize(gradient_method)(self.biases)

