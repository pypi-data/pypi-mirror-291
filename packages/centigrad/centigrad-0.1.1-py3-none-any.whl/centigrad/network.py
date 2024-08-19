from .layer import Layer
from tqdm import tqdm
import numpy as np

class Network:
    """
    Initializes a neural network where the layers are Layer objects

    Parameters:
    -----------
    input_dim (int): The dimension of the input layer.
    layers_widths (list of int): A list where each element represents the number of neurons in each layer of the network.
    layers_activations (list of str): A list of activation functions corresponding to each layer. The length must match `layers_widths`.
    cost_function (str, optional): The cost function to use. Defaults to "mse".
    initial_weights (list of numpy.ndarray, optional): Initial weights for each layer. Should match the dimensions specified. Defaults to None.
    initial_biases (list of numpy.ndarray, optional): Initial biases for each layer. Should match the dimensions specified. Defaults to None.
    
    Raises:
    -------
    ValueError: If the length of `layers_widths` is zero or does not match the length of `layers_activations`.
    """
    def __init__(self, 
                 input_dim, 
                 layers_widths, 
                 layers_activations, 
                 cost_function = "mse", 
                 initial_weights = None,
                 initial_biases = None):
        
        if (len(layers_widths)>0) & (len(layers_widths)==len(layers_activations)):
            self.depth = len(layers_widths)
            self.layers_widths = layers_widths
            self.layers_activations = layers_activations
            self.cost_function = cost_function
            self.layers = []
            for idx, val in enumerate(layers_widths):
                if len(self.layers)==0:
                    input_dim_layer = input_dim
                else: input_dim_layer = layers_widths[idx-1]
                self.layers.append(Layer(input_dim = input_dim_layer,
                                         n_neurons = val, 
                                         activation = layers_activations[idx],
                                         initial_weights = initial_weights[idx] if initial_weights is not None else None,
                                         initial_biases = initial_biases[idx] if initial_biases is not None else None))
        else:
            raise("The network should be at least 1 layer deep and dimensions the length of layers_widths should match  the length of layers_activations.")
    
    
    def cost(self,X, y):
        """
        Computes the cost of the network's predictions using the specified cost function and current weights.

        Parameters:
        -----------
        X (numpy.ndarray): The input data.
        y (numpy.ndarray): The true labels or target values.
        
        Returns:
        --------
        float: The computed cost.
        """
        prediction = self.forward(X)
        if self.cost_function == "mse":
            return (((prediction - y)**2).sum().value)/(y.shape[1])
                      
    def forward(self, input_data):
        """
        Performs a forward pass through the network.

        Parameters:
        -----------
        input_data (numpy.ndarray): The input data to the network.
        
        Returns:
        --------
        numpy.ndarray: The output of the network after the forward pass.
        """
        for layer in self.layers:
            input_data = layer.forward(input_data)
        return input_data
    
    def fit(self, X, y, epochs, learning_rate):
        """
        Trains the neural network by iteratively adjusting the weights and biases
        using backpropagation over a specified number of epochs.
        
        Parameters:
        -----------
        X : np.ndarray
            The input data for training.
        y : np.ndarray
            The target labels corresponding to the input data.
        epochs : int
            The number of iterations to train the neural network.
        learning_rate : float
            The step size used for updating the weights and biases during training.
        
        Returns:
        --------
        self : object
            Returns the instance of the model after training.
        """
        epoch_losses = [self.cost(X, y)]
        for _ in tqdm(range(epochs)):
            for lay in self.layers:
                gradients = lay.backward()
                lay.weights = lay.weights - learning_rate*gradients[0]
                lay.biases = lay.biases - learning_rate*gradients[1]
            epoch_losses.append(self.cost(X,y))
        self.epoch_losses = epoch_losses
        return self
    
    def predict(self, X):
        """
        Makes predictions on the input data using the trained neural network.
        
        Parameters:
        -----------
        X : np.ndarray
            The input data for which predictions are to be made.
        
        Returns:
        --------
        np.ndarray
            The predicted output values for the input data.
        """
        output = X
        for layer in self.layers:
            output = layer.forward(output)
        
        return output
        