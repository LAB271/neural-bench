from neural_bench.network import Network
from neural_bench.fc_layer import FCLayer
from neural_bench.quantized_layer import QuantizedLayer
from neural_bench.activation_layer import ActivationLayer
from neural_bench.activations import tanh, tanh_prime
from neural_bench.losses import mse, mse_prime

from keras.datasets import mnist
#from keras.utils import to_categorical
from keras import utils as np_utils
import numpy as np

SIZE=2000
LENGTH=10

def prep_data():
    # load MNIST from server
    print("Loading MNIST ....")
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    print("Prep data")
    # training data : 60000 samplesß
    # reshape and normalize input data
    x_train = x_train.reshape(x_train.shape[0], 1, 28*28)
    x_train = x_train.astype('float32')
    x_train /= 255
    # encode output which is a number in range [0,9] into a vector of size 10
    # e.g. number 3 will become [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    y_train = np_utils.to_categorical(y_train)

    # same for test data : 10000 samples
    x_test = x_test.reshape(x_test.shape[0], 1, 28*28)
    x_test = x_test.astype('float32')
    x_test /= 255
    y_test = np_utils.to_categorical(y_test)
    return (x_train, x_test), (y_train, y_test)

def train_network(train_in, train_out):
    # Network
    net = Network()
    net.add(FCLayer(28*28, 100))                # input_shape=(1, 28*28)    ;   output_shape=(1, 100)
    net.add(ActivationLayer(tanh, tanh_prime))
    net.add(FCLayer(100, 50))                   # input_shape=(1, 100)      ;   output_shape=(1, 50)
    net.add(ActivationLayer(tanh, tanh_prime))
    net.add(FCLayer(50, 10))                    # input_shape=(1, 50)       ;   output_shape=(1, 10)
    net.add(ActivationLayer(tanh, tanh_prime))

    # train on 1000 samples
    # as we didn't implemented mini-batch GD, training will be pretty slow if we update at each iteration on 60000 samples...
    net.use(mse, mse_prime)
    print('Start training')
    net.fit(train_in, train_out, epochs=35, learning_rate=0.1)
    return net

def quantize(net):
    net2 = Network()
    net2.add(QuantizedLayer(net.layers[0]))
    net2.add(ActivationLayer(tanh, tanh_prime))
    net2.add(QuantizedLayer(net.layers[2]))
    net2.add(ActivationLayer(tanh, tanh_prime))
    net2.add(QuantizedLayer(net.layers[4]))
    net2.add(ActivationLayer(tanh, tanh_prime))
    return net2

if __name__ == '__main__':
    train, validate = prep_data()
    net = train_network(train[0][0:SIZE], validate[0][0:SIZE])
    # net2 = quantize(net)

    # test on 3 samples
    out = net.predict(train[1][0:LENGTH])
    # out2 = net2.predict(train[1][0:LENGTH])
    print("\n")
    print("predicted values : ")
    for r in out:
        print(np.argmax(r), end="\n")
    # print("quantized values : ")
    # for r in out2:
    #     print(np.argmax(r), end="\n")
    print("true values : ")
    print(validate[1][0:3])
