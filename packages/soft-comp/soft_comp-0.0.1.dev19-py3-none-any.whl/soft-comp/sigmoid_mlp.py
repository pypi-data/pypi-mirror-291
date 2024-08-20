""" Simple Multi Layer Perceptron (MLP) with sigmoid activation functions. """
__author__    = "Christian Gruhl"
__copyright__ = "© 2024 Universität Kassel"

import numpy as np

def one_hot(clazz, num):
    return np.eye(num)[clazz]

def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    return sigmoid(z) * (1-sigmoid(z))

class NeuralNet:

    def __init__(self, sizes, random_state=None):
        """ Erzeugt und initialisiert die Schichten eines MLP.
            Die Parameter sind standardnormalverteilt

            sizes         - [num_neurons] Enthaelt die Anzahl
                            an Neuronen pro Schicht
            random_state  - seed fuer den PRNG
        """
        self.rng = np.random.default_rng(random_state)
        self.sizes = sizes
        self.num_layers = len(self.sizes)
        # Schwellwerte zufaellig initialisieren
        self.biases = [self.rng.normal(size=num) for num in self.sizes[1:]]
        # Gewichte zufaellig initialisieren
        self.weights = [self.rng.normal(size=(num_s, num_p))
                         for num_p, num_s in zip(self.sizes[:-1], self.sizes[1:])]
    def forward(self, x):
        # a ist die Aktivierung der "vorherigen" Schicht
        # und entsprocht initial der Eingabe
        a = x
        # Schleife durch alle Schichten
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w,a) + b
            a = sigmoid(z)
        # Aktivierung der letzten Schicht entspricht
        # der Netzausgabe
        return a

    def predict(self, X):
        """ X - Muster die Klassifiziert werden sollen
         Returns: dezimal kodierte Klassen """
        return np.argmax([self.forward(x) for x in X], axis=1)
    
    def __call__(self, X):
        return self.predict(X)
    
    def eval(self, X, y):
        """ Berechnet die Genauigkeit/Accuracy """
        return (self.predict(X) == np.argmax(y,axis=1)).sum()/len(X)

    def SGD(self, X, y, epochs, mini_batch_size, eta, train_error=False, test_data=None):
        """ Stochastic Gradient Descent fuer MLP
            Erzeugt die mini batches und ruft die Update-Funktion auf

            X               - Trainingsdaten
            y               - Labels
            epochs          - Anzahl an Trainingsepochen
            mini_batch_size - Groesse m der mini batches
            eta             - Lernrate
        
        """
        self.train_error = [] # Fuer Analyse
        self.test_error = []  # Fuer Analyse
        self.eta = eta
        n = len(X)
        for j in range(epochs):
            idx = np.arange(len(X))
            self.rng.shuffle(idx)
            self.mini_batches = [[X[idx][k:k+mini_batch_size],
                                  y[idx][k:k+mini_batch_size]]
                                  for k in np.arange(0, n, mini_batch_size)]
            for mini_batch in self.mini_batches:
                self.update_mini_batch(mini_batch)
            if train_error:
                err = 1 - self.eval(X,y) # Fehlerberechnen
                self.train_error.append(err)
                print("Epoche %d Train Error %.3f" % (j, err))
            if test_data is not None:
                self.test_error.append(1-self.eval(test_data[0],test_data[1]))

    def update_mini_batch(self, mini_batch):
        """ Implementierung der Update-Regeln
            mini_batch - (M, y) Auswahl an Beispielen und Labeln
        """
        # Berechnen der Gradientenvektoren der letzten Schicht
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        # Berechnen der neuen Gradientenvektoren
        for x_i, y_i in zip(*mini_batch):
            delta_nabla_b, delta_nabla_w = self.backprop(x_i, y_i)
            # Aggregieren um spater Mittelwert zu bilden
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        
        # Die "bekannten" Update-Regeln fuer SGD
        self.weights = [w - (self.eta/len(mini_batch))*nw for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - (self.eta/len(mini_batch))*nb for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # feedforward
        activation = x
        activations = [x] 
        zs = [] 
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        
        # backward pass
        delta = self.cost_derivative(activations[-1], y) * sigmoid_prime(zs[-1]) #BP1
        nabla_b[-1] = delta
        nabla_w[-1] = np.outer(delta, activations[-2])

        for l in np.arange(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].T, delta) * sp #BP2
            nabla_b[-l] = delta #BP3
            nabla_w[-l] = np.outer(delta, activations[-l-1]) #BP4
        return nabla_b, nabla_w

    def cost_derivative(self, output_activations, y):
        return (output_activations-y)
