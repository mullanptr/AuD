import numpy as np

debug_w0 = np.array([[0.13436424411240122, 0.8474337369372327]])
debug_b0 = np.array([[0.763774618976614]])

debug_w1 = np.array([[0.2550690257394217],
            [0.4494910647887381]
            ])
debug_b1 = np.array([[0.49543508709194095],
            [0.651592972722763]
            ])

class sigmoid():

    def __init__(self):
        self.fct = np.vectorize(lambda x: 1 / ( 1 + np.exp(-x)))

    def activate(self, input_data):
        return self.fct(input_data)

    def derivative(self, x):
        # equiv. to: sig(x)/dx = sig(x) * (1 - sig(x))
        return x * (1.0 - x)

class fully_connected_layer():

    weights = None
    biases = None
    y_pred = None
    err = None
    epochs_trained = 0

    def __str__(self):
        s =  ''
        s += '\tweights:\n'
        s += str(self.weights)
        s += '\n\tbiases:\n'
        s += str(self.biases)
        s += '\n\ty_pred:\n'
        s += str(self.y_pred)
        s += '\n\terr:\n'
        s += str(self.err)
        s += '\n\tepochs_trained: {self.epochs_trained}'
        return s

    def __init__(self, input_len, output_len):
        self.weights = np.array([np.random.rand(input_len) for _ in range(output_len)]).T
        self.biases = np.array([np.random.rand(1) for _ in range(output_len)]).T

        self.activation = sigmoid()

    def predict(self, input_data):
        res = np.matmul(input_data, self.weights) + self.biases
        res = self.activation.activate(res)
        self.y_pred = res
        return res

    def backprop(self, err):
        self.err = np.matmul(self.weights, err.T)
        self.epochs_trained += 1
        return self.err

class model():

    def __str__(self):
        s = ''
        for i, l in enumerate(self.layers):
            s += f'Layer {i}:\n'
            s += str(l)
            s += '\n###################################\n'
        return s

    def __init__(self,layers=[2,3,1], random_state=1, loss_fct=lambda y_true, y_pred: y_true - y_pred):
        np.random.seed(random_state)
        self.layers = [fully_connected_layer(input_len=i, output_len=j) for i,j in zip(layers[:-1], layers[1:])]
        self.loss_fct = loss_fct

    def predict(self,input_data):
        for i, l in enumerate(self.layers):
            input_data = l.predict(input_data)
        return input_data

    def loss(self, y_true, y_pred):
        return self.loss_fct(y_true, y_pred)

    def backprop(self, y_true, y_pred):

        err = self.loss(y_true, y_pred)
        for i, l in enumerate(self.layers[::-1]):
            derivatives = l.activation.derivative(l.y_pred)
            deltas = err * derivatives
            l.err = err
            l.deltas = deltas
            err = np.matmul(l.weights, deltas.T)

if __name__ == '__main__':

    m = model()

    m.layers[0].weights = debug_w0.T
    m.layers[0].biases  = debug_b0.T
    m.layers[1].weights = debug_w1.T
    m.layers[1].biases  = debug_b1.T

    p = m.predict(np.array([[1,0]]))
    m.backprop([[0,1]], p)

    X = np.array([
            [1,0],
            [1,0],
            [1,1],
            [0,1],
        ])

    y = np.array([
            [0],
            [0],
            [1],
            [1],
        ])

    batch_size = 1
    p = m.predict(X[:batch_size,:])
