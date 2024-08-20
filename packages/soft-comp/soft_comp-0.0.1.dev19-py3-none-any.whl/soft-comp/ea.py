""" Evolutionary Algorithms """
__author__    = "Christian Gruhl"
__copyright__ = "© 2024 Universität Kassel"
import numpy as np

def mutate_gauss(X, sigma, m_rate, limits):
    """ X - Individuum (Vektor von reelen Zahlen)
        sigma - Standardabweichung
        m_rate - Mutationsrate
        limits - Wertebereiche [[min,max], ...] """
    for i,x_i in enumerate(X):
        if np.random.random() <= m_rate:
            u = np.random.normal(scale=sigma)
            X[i] = x_i + u
            X[i] = np.maximum(X[i], limits[i][0])
            X[i] = np.minimum(X[i], limits[i][1])

    return X

def mutate_int(X, sigma, m_rate, limits):
    return np.asarray([ int(x) for x in mutate_gauss(X, sigma, m_rate, limits)])

def sd_linear(sd, ranking):
    """ Lineares Ranking"""
    lranks = np.asarray(2 - sd + 2* (sd-1) * (np.arange(len(ranking))[::-1]/len(ranking)))
    # normalisieren - sum(lranks) = 1
    return lranks/lranks.sum()

def roulette_selection(pop, f_pop, sd, size):
    """ Rouletteselektion """
    rank = np.argsort(f_pop)
    idx = np.asarray([np.random.choice(len(pop), size=2, p=sd_linear(sd, rank)) for _ in range(size)])
    return pop[idx]

def reinsertion(population, offspring, f, omega):
    """ population - Aktuelle Population
        offspring  - Nachkommen (haengt von gamma ab)
        f          - Fitnessfunktion
        omega      - Wiedereinfuegerate """
    # HERE WAS A BUG FIXME IN LECTURE!!!!
    idx_off = np.argsort(f(offspring))[::-1]
    idx_pop = np.argsort(f(population)) # Invertiert
                                              # siehe :14
    n = int(np.ceil(omega * len(population)))

    next_generation = np.vstack((offspring[idx_off[:n]],
                                population[idx_pop[n:]]))
                                

    return next_generation

def single_point_cross_over(X_mother, X_father):
    """ X_mother - erster Elter
        X_father - zweiter Elter """
    point = np.random.randint(0,len(X_mother))

    child = np.zeros_like(X_mother) 
    child[:point] = X_mother[:point]
    child[point:] = X_father[point:]

    return child

def mutate_bit(X, m_rate):
    """ X - Individuum (Bitfolge)
    m_rate - Mutationsrate """
    for i, x_i in enumerate(X):
        if np.random.random() <= m_rate:
            X[i] = bool(1 - x_i)
    return X