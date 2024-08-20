""" Perceptron """
__author__    = "Christian Gruhl"
__copyright__ = "© 2024 Universität Kassel"
import numpy as np

###############################################################################
#                                                                             #
#                                  Perceptron                                 #
#                                                                             #
###############################################################################
class perceptron:
    """ Simple implementation of a perceptron """
    def __init__(self, rng, dims=2):
        """
        Parameters
        ----------
        rng : numpy.random._generator.Generator
            Random number generator to draw initial weights
        """
        self.w = rng.random(dims)
        self.b = 0 
    
    def __call__(self, x):
        """ Calculates f(wx-b), i.e. the output of the perceptron
        
        Parameters
        ----------
        x : ndarray
            input x

        Returns
        -------
        f(z) : int
        
        """
        z = np.dot(self.w, x) - self.b
        return 1 if z > 0 else 0
    
    def predict(self, X):
        """ Calculate output for multiple observations.
        
        Parameters
        ----------
        X : ndarray(:,x)
            Observations, one per row, features are in columns

        Returns
        -------
        f(X) : ndarray()
            Predictions for each observation
        """
        return np.asarray([self(x) for x in X])
        
    def fit(self, X, y, eta=0.1, epochs=10):
        """ Execute the perceptron learning algorithms for given epochs.
        
        Parameters
        ----------
        X : ndarray(N,d)
           Training data
        y : ndarray(N)
           Labels (only 1 and 0 are supported)
        """
        for epoche in range(epochs):
            for x_i, y_i in zip(X, y):
                y_pred = self(x_i)
                error = y_i - y_pred
                delta = eta * error * x_i                
                self.w += delta
                self.b -= eta * error
                
###############################################################################
#                                                                             #
#                           Mark 1 Perceptron                                 #
#                                                                             #
###############################################################################

class Mark1Perceptron:
    """ Software implementation of a Mark 1 Perceptron. """

    def __init__(self, num_s_units, num_a_units, num_r_units, theta, epochs=2000, p=[.20,.20,.6], random_state=None):
        """
        Parameters
        ----------
        num_s_units : int
            Sensory Units: These are randomly connected to the A-Units. They recieve the input, i.e. an image.
        num_a_units : int
            Association Units: Hidden layer. Connected to R-Units. Weights from A to R-Units are learned.
        num_r_units : int
            Response Units: Output units, i.e. classes in one-against-all fashion.
        theta : int
            Threshold for A-Units. My assume values from 1 to 7
        epochs : int, default=2000
        p : [float], default=[.20,.20,.6]
            Probabilities for connections and weights between S and A. Either (weights) -1, +1, or (not connected) 0
        random_state : rng | None

        """
        self.rng = np.random.default_rng(random_state)
        self.theta = theta
        self.epochs=epochs
        self.A = self.rng.choice([-1,1,0], p=p, replace=True, size=(num_s_units, num_a_units))
        self.R = [perceptron(self.rng, dims=num_a_units) for _ in range(num_r_units)]


    def s_to_a(self, x):
        return np.multiply(self.A,x[:,np.newaxis])
    
    def prop(self, x):
        """ Propagate input throug S-Units to A-Units """
        return (self.s_to_a(x).sum(axis=0) > self.theta).astype(int)
    
    def fit(self, X, y):
        """ Adjust the weights of the connections between A and R-Units.
        
        Parameters:
        -----------
        X : ndarray(N,d)
            Observations
        y : ndarray(N,R)
            Labels, one-hot encoded, must match R-Units
        
        """
        X_prop = np.asarray([self.prop(x) for x in X])
        for i, r_unit in enumerate(self.R):
            # one-vs-rest training
            r_unit.fit(X_prop, y[:,i])

    def predict(self, X):
        """ Predict outputs for all observations in X
        
        Parameters
        ----------
        X : ndarray(N,d)
            Observations

        Returns
        -------

        """
        X_prop = np.asarray([self.prop(x) for x in X])
        return np.asarray([[r_unit(x) for r_unit in self.R] for x in X_prop])
