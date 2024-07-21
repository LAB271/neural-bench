
import numpy as np

# activation function and its derivative
def tanh(x):
    return np.tanh(x)

def tanh_prime(x):
    return 1-np.tanh(x)**2


# some more
def gelu(x):
    return 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * np.power(x, 3))))

def gelu_prime(x):
    sqrt_2_pi = np.sqrt(2 / np.pi) 
    tanh_term = np.tanh(sqrt_2_pi * (x + 0.044715 * np.power(x, 3))) 
    derivative_tanh_term = (1 - np.power(tanh_term, 2)) * sqrt_2_pi * (1 + 3 * 0.044715 * np.power(x, 2)) 
    return 0.5 * (1 + tanh_term + x * derivative_tanh_term)