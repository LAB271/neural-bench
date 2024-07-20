import sys

BAR_LENGTH=20

class Network:
    def __init__(self):
        self.layers = []
        self.loss = None
        self.loss_prime = None

    # add layer to network
    def add(self, layer):
        self.layers.append(layer)

    # set loss to use
    def use(self, loss, loss_prime):
        self.loss = loss
        self.loss_prime = loss_prime

    # predict output for given input
    def predict(self, input_data):
        # sample dimension first
        samples = len(input_data)
        result = []

        # run network over all samples
        for i in range(samples):
            # forward propagation
            output = input_data[i]
            for layer in self.layers:
                output = layer.forward_propagation(output)
            result.append(output)

        return result

    # train the network
    def fit(self, x_train, y_train, epochs, learning_rate):
        # sample dimension first
        samples = len(x_train)

        # training loop
        for i in range(epochs):
            err = 0
            for j in range(samples):
                # forward propagation
                output = x_train[j]
                for layer in self.layers:
                    output = layer.forward_propagation(output)

                # compute loss (for display purpose only)
                err += self.loss(y_train[j], output)

                # backward propagation
                error = self.loss_prime(y_train[j], output)
                for layer in reversed(self.layers):
                    error = layer.backward_propagation(error, learning_rate)

            # calculate average error on all samples
            err /= samples
            self.print_progress(i+1, epochs, err)


    # print_progress() : Displays or updates a console progress bar
    ## https://stackoverflow.com/questions/3160699/python-progress-bar/3162864
    def print_progress(self, epoch, max_epoch, err):
        status = "error: {0:.4f}".format(err)
        if epoch >= max_epoch:
            status = "Done...               \r\n"
        block = int(round(BAR_LENGTH*epoch/max_epoch))
        text = "\rTraining: [{0}] {1:2}/{2} {3}".format( "#"*block + "-"*(BAR_LENGTH-block), epoch, max_epoch, status)
        sys.stdout.write(text)
        sys.stdout.flush()