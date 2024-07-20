from neural_bench.layer import Layer
import numpy as np

# inherit from base class Layer
class QuantizedLayer(Layer):
    # input_size = number of input neurons
    # output_size = number of output neurons
    def __init__(self, layer):
        self.scale_weights = (np.max(layer.weights)-np.min(layer.weights))/256
        self.weights = (layer.weights/self.scale_weights).astype(int)
        # self.scale_bias = (np.max(layer.bias)-np.min(layer.bias))/256
        # self.bias = (layer.bias/self.scale_bias).astype(int)
        # print(self.scale_weights, self.scale_bias)

    # returns output for a given input
    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = np.dot(self.input, self.weights*self.scale_weights)
        # self.output = np.dot(self.input, self.weights*self.scale_weights) + self.bias*self.scale_bias
        return self.output