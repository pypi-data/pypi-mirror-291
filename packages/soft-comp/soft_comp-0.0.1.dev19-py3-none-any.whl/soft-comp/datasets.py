""" Datasets """
__author__    = "Christian Gruhl"
__copyright__ = "© 2024 Universität Kassel"
import numpy as np
import cartopy.geodesic as cgeo

###############################################################################
#                                                                             #
#                 Traveling Salesperson Problem (TSP)                         #
#                                                                             #
###############################################################################

def tsp_cities():
    """ European cities for Travelling Sales Person example.
    
    Returns
    -------
    (city_names, city_locations, distances)
        Name of the cities, their locations as longitude/latitude, distances between cities in KM.

    """
    # rough city locations
    cities = {
        "London": (-0.1278, 51.5074),
        "Paris": (2.3522, 48.8566),
        "Berlin": (13.4050, 52.5200),
        "Madrid": (-3.7038, 40.4168),
        "Rome": (12.4964, 41.9028),
        "Athens": (23.7275, 37.9838),
        "Stockholm": (18.0686, 59.3293),
        "Oslo": (10.7522, 59.9139),
        "Warsaw": (21.0122, 52.2297),
        "Amsterdam": (4.9041, 52.3676),
        "Vienna": (16.3738, 48.2082),
        "Dublin": (-6.2603, 53.3498),
        "Prague": (14.4378, 50.0755),
        "Brussels": (4.3517, 50.8503),
        "Budapest": (19.0402, 47.4979),
        "Lisbon": (-9.1393, 38.7223),
        "Helsinki": (24.9384, 60.1695),
        "Copenhagen": (12.5683, 55.6761),
        "Zurich": (8.5417, 47.3769),
        "Reykjavik": (-21.9426, 64.1466),
        "St Petersburg": (30.3351, 59.9343)
    }

    city_array =  np.array(list(cities.values()))

    # calculate pairwise distances in km
    geodesic = cgeo.Geodesic()
    distances = np.asarray([np.round(geodesic.inverse(city, city_array)[:,0]/1000, decimals=-1) for city in city_array], dtype=int)
    
    return cities.keys(), city_array, distances


def tsp_fitness(sol, cost_matrix):
    # Roundtrip! Last city must be the first one!
    penalty = len(set(np.arange(len(sol))).difference(set(sol)))
    return -np.log(np.sum([cost_matrix[i,j] for i,j in zip(sol,np.concatenate((sol[1:], sol[:1])))])) - penalty

###############################################################################
#                                                                             #
#                            Knapsack Problem                                 #
#                                                                             #
###############################################################################

def rucksack_items(num, random_state=None):
    """ Generate random weights for Rucksack items.
    
    Parameters
    ----------
    num : int
        Number of items to generate
    random_state : int
        Seed for rng

    Returns
    -------
    ndarray (num,2)
        Random values and weights for num items
    """
    rng = np.random.default_rng(random_state)
    values = rng.integers(0,25,size=num).T
    weights = rng.integers(1,50,size=num).T

    return np.vstack((values, weights)).T

def sol2dec(sol_in):
    return np.sum([ v*2**i for i,v in enumerate(sol_in[::-1])])

def dec2sol(dec_in, width=8):
    return np.array(list(np.binary_repr(dec_in,width=width)),dtype=int).astype(bool)

def fitness_rucksack(items, solution, capacity):
    return items[solution,0].sum() if items[solution,1].sum() <= capacity else capacity - items[solution,1].sum()
