""" Fuzzy Logic """
__author__    = "Christian Gruhl"
__copyright__ = "© 2024 Universität Kassel"

import numpy as np
import matplotlib.pyplot as plt
from enum import IntEnum

# Macros are for lecture slides.

###############################################################################
#                                                                             #
#                          Membership Functions                               #
#                                                                             #
###############################################################################


def triangular(a, b, c):
    return lambda x: np.maximum(0, np.minimum((x - a) / (b - a), (c - x) / (c - b)))

def trapezoidal(a, b, c, d):
    return lambda x: np.maximum(0, np.minimum((x - a) / (b - a), np.minimum(1, (d - x) / (d - c))))

def gaussian(m, sigma):
    return lambda x: np.exp(-(x - m) ** 2 / (sigma ** 2))

def sigmoid(m, a):
    return lambda x: 1 / (1 + np.exp(-a * (x - m)))

def singleton(x, m):
    return lambda x: (np.abs(x-m) < 1e-9).astype(float)

def z_shape(a, b):
    # source z-shape: https://www.mathworks.com/help/fuzzy/zshapedmf.html
    def ret(x) :
        left = np.where(x <= a, 1, 0)
        middle = np.where(np.logical_and(a <= x, x <= (a+b)/2), 1-2*((x-a)/(b-a))**2,0)   
        right = np.where(np.logical_and((a+b)/2 <= x, x <= b), 2*((x-b)/(b-a))**2,0)
        return np.maximum(left, np.maximum(right, middle))
    return ret

###############################################################################
#                                                                             #
#                        Defuzzyfication Functions                            #
#                                                                             #
###############################################################################
def centre_of_mass( mu , supp , dx =0.01):
    ys = np.arange(supp[0], supp[1], dx)
    mu_ys = mu(ys)
    mu_ys_sum = mu_ys.sum()
    return (ys * mu_ys).sum()/mu_ys_sum if mu_ys_sum > 0 else 0

###############################################################################
#                                                                             #
#                         Mamdani Fuzzy System                                #
#                                                                             #
###############################################################################
def plot_linguistic_variable(var, dx=0.1):
    """ Plot the given lingustic variable.
    Each term membership function is plotted, the support is determined by the
    '_support' field if present.
    parameters
    ----------
    var : dict
       Dicitonary containing the lingustic terms as keys and their
       corresponding membership functions as values
    dx : float
       Sampling rate for plotting
    """
    sup = var.get('_support', [-1,1])
    xs = np.arange(sup[0],sup[1]+dx,dx)

    [plt.plot(xs, mu(xs), label=key) for key,mu in var.items() if key[0] != '_']
    plt.legend()
    plt.xlim(*sup)

def IF(*AND, THEN=None, infer_op=np.fmin, and_op=np.min):
    """ Function to create executable (lambda function) rules.

    The premise can consist of multiple tuples. The THEN parameter is used for the
    inference rule, i.e. mapping an output variable to an linguistic term.

    Parameters
    ----------
    AND : (var_idx, mu_term)*
        Premise, can consists of multiple conjunction of tuples. 
    THEN : (var_id, mu_term) | None
        If set to None, this functions returns the premise as lambda function
        λ x →  ∧ µ(x))
    infer_op : 
        Operation to use for inference/implication 
        Default is MIN
    and_op :
        Operation to use for AND (see t-Norm in the lecture)
        Default is MIN

    Returns
    -------
        A function that takes an observation as input and returns the conclusion membership function µ (λ x → (y, µ_y(x)) ) of the rule,
        where y is the index of the output variable and µ_y the corresponding conclusion.
        OR if the THEN clause is None the activiation of the rule, i.e. the premise, is returned: λ x →  ∧ µ(x))
    
    """

    #return lambda x : (y_idx, lambda y : infer(and_op([ mu(x[x_idx]) for (x_idx, mu) in AND]), mu_y(y)))
    if len(AND) == 1 and callable(*AND):
        premise=AND[0]
    else:
        premise = lambda x : and_op([ mu(x[x_idx]) for (x_idx, mu) in AND])
    
    if THEN is None:
        return premise
    else:
        (y_idx, mu_y) = THEN
        return lambda x : (y_idx, lambda ys : infer_op(premise(x), mu_y(ys)))



def make_rule_inference(Rules:list, Y:IntEnum, infer_op=lambda x : np.max(x, axis=0)):
    """ Generate a function that takes an observation as input and
    evaluate all Rules. There are multiple conclusions returned, one for each output variable
    specified by Y.
    
    Parameters
    ----------
    Rules : [Rule]
        List of rules generated with the IF funktion
    Y : IntEnum
        Output variables, i.e. those controlled by the fuzzy system
    infer_op:
        The operation used to combine the conclusions of the different rules.
        Default is MAX

    Returns
    -------
        λ x → dict(y, λ ys → µ_y(ys))
        Inference function to get the conclusion functions for all outputs y based on the given input x

    """

    # construct the inference function which is returned
    def inference(x):
        # Intermediate result, stores the output conclusions of all rules for the given input x
        Z = np.asarray([R(x) for R in Rules])
        # the outer lambda is necessary to create a closure that stores the selected fuzzy functions (funs)
        return {out_var : (lambda funs :
                             lambda ys : infer_op([f(ys) for f in funs])) # create the infered conclusion function, which is the value of the returned dictionary
                             (Z[Z[:,0] == out_var,1]) # bind the conclusion functions for a single output variable to "funs"
                             for out_var in Y if out_var in Z[:,0]} # iterate over all valid output variables (valid=at least one rule provides a conclusion)

    return inference

def make_inference(Rules, out_vars):
    """ Create a fuzzy inference system based on the given ruleset to control the out_vars of a system.

    Parameters
    ----------
    Rules : [Rule]
        List of rules generated with the IF funktion
    out_vars : dict(IntEnum:dict)
        Mapping from output variables (IntEnum) to linguistic variables (dict)
    Returns
    -------
    λ x → dict(y, ŷ)
        A function that takes an input x and calculates the defuzzyfied control outputs (values) for
        each output variable (key) as a dict.
    
    """
    y_mus_f = make_rule_inference(Rules, out_vars.keys())

    # the inner lambda is to bind y_mus
    return lambda x : (lambda y_mus : {v : centre_of_mass(y_mus[v], out_vars[v]['_support']) for v in out_vars.keys() if v in y_mus})(y_mus_f(x))
