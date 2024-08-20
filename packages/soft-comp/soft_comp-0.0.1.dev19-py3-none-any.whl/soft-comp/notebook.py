""" Helper and interactive plots for notebook exercises """
__author__    = "Christian Gruhl"
__copyright__ = "© 2024 Universität Kassel"

import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interact, interactive, interact_manual
from softcomputing.perceptron import perceptron
import networkx as nx

###############################################################################
#                                                                             #
#                     SLP/PerceptronTraining.ipynb                            #
#                                                                             #
###############################################################################

# Code für interaktives Experimentieren
def f(w,b,f_z):
    xs = np.arange(-2,2,.01)
    plt.title("w=%.2f b=%.2f" % (w,b))
    plt.plot([-2,2],[b, b], 'm')
    plt.plot(xs, np.dot(w,xs), 'c', zorder=5)
    if f_z:
        cut = b/w if w != 0 else (-2 if w > b else 2)
        plt.fill_between(np.arange(-2,cut,.01),-1,1, color='m', alpha=.1, hatch='xx', label='$f(z)=0$')
        plt.fill_between(np.arange(cut,2,.01),-1,1, color='g', alpha=.1, hatch='xx', label='$f(z)=1$')
        plt.legend()
    else:
        plt.fill_between(xs, -1, b, color='k', hatch="//", alpha=.1)
        plt.fill_between(xs, b, 1, color='g', hatch="xx", alpha=.1)
    plt.plot([0,0],[-1,1],':k')
    plt.plot([-2,2],[0,0],':k')
    plt.xlabel("x")
    plt.ylabel("$w\cdot x$")
    plt.xticks([-1,0,1])
    plt.yticks([-1,0,1])
    plt.ylim([-1,1])
    plt.xlim([-2,2])
    
    plt.tight_layout()

interactive_perceptron_wb = lambda : interact(f, w=(-.5,.5,.01), b=(-.5,.5,.01), f_z=False)

# Code für Interaktives Experimentieren
def g(p_test, eta, X, y):
    try:
        g.epoche_counter += 1
    except AttributeError:
        g.epoche_counter = -1

    if g.epoche_counter > 0 and X is not None and y is not None:
        p_test.fit(X, y, eta, 1)
    xs = np.arange(-1,3,0.01)
    X1,X2 = np.meshgrid(xs,xs)
    Theta = np.vstack([X1.ravel(), X2.ravel()]).T
    booleans = np.asarray([[0,0],[0,1],[1,0],[1,1]])
    
    plt.figure()
    plt.title("Epoche %d" % g.epoche_counter)
    Z_p_test = np.asarray( [p_test(x) for x in Theta] ).reshape(len(xs),len(xs))
    
    plt.scatter(*booleans.T, marker='o', edgecolor='k', c='m')
    plt.contour(xs, xs, Z_p_test, levels=0, colors='k')

    plt.xticks([0,1])
    plt.yticks([0,1])
    plt.xlim([-0.1,1.1])
    plt.ylim([-0.1,1.1])
    plt.xlabel("$x_1$")
    plt.ylabel("$x_2$")

    plt.tight_layout()
    plt.show()

def interactive_perceptron(perceptron_in, eta=None, X=None, y=None):
    if perceptron_in is not None:
        interact_manual(lambda : g(perceptron_in, eta, X, y))

###############################################################################
#                                                                             #
#                        MLP/SigmoidNeuron.ipynb                              #
#                                                                             #
###############################################################################
def h(x,delta_w, delta_b):
    class sigmoid:
        def __init__(self, w, b):
            self.w = w
            self.b = b
        
        def __call__(self, x):
            return 1/(1+np.exp(-self.w*x-self.b))
    
        def update_w(self, delta_w):
            self.w += delta_w
    
        def update_b(self, delta_b):
            self.b += delta_b
    
        def __str__(self):
            return "w: %.2f b: %.2f" % (self.w, self.b)
    xs=np.arange(-10,10,.1)
    s = sigmoid(1,0)
    plt.figure()
    plt.plot(xs, s(xs), 'k', label="$\sigma(z)$")
    plt.vlines(x,0,1, colors='c', linestyles='--')
    s_x = s(x)
    s.update_w(delta_w)
    s.update_b(delta_b)
    plt.plot(xs, s(xs), '--m', label="$\sigma^*(z)$")
    delta_s_x = np.abs(s_x - s(x))
    plt.title("$\Delta w$: %.1f $\Delta b$: %.1f - %s - $\Delta \sigma(z|x=%.1f):%.2f$" % (delta_w, delta_b, s, x, delta_s_x))
    plt.legend()
    plt.tight_layout()
    plt.show()
    
interactive_sigmoid = lambda : interactive(h,x=(-10,10,.1),delta_w=(-1,2,.1),delta_b=(-5,5,.1))

###############################################################################
#                                                                             #
#                          MLP/Topologie.ipynb                                #
#                                                                             #
###############################################################################
def show_adjacency_network(A):
    plt.figure()
    plt.title("Adjazenz-Matrix Topologie")
    G = nx.from_numpy_array(A)
    pos = {
        0: (0, 2),   # Input node 1
        1: (0, 1),   # Input node 2
        2: (0, 0),   # Input node 3
        3: (1, 2.5), # Hidden node 1
        4: (1, 1.5), # Hidden node 2
        5: (1, 0.5), # Hidden node 3
        6: (1, -0.5),# Hidden node 4
        7: (2, 1),   # Output node
    }
    nx.draw(G, pos, with_labels=True, node_color='#C4D20F', node_size=700, edge_color='#C7105C')
    edge_labels = {(u, v): f"{G[u][v]['weight']:.2f}" for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=.8)
    plt.show()

###############################################################################
#                                                                             #
#                       MLP/GradientDescent.ipynb                             #
#                                                                             #
###############################################################################
def gd(v, eta):
    f = lambda x : 0.1*x**4 + .5*x**3 + .4*x**2 + .1*x + 5
    f_p = lambda x : (4*0.1)*x**3 + (3*.5)*x**2 + (2*.4)*x + .1
    dir_arrow = ["","→", "←"]

    vs = np.arange(-5,4,.1)
    plt.plot(vs,f(vs),'m', label="$f(v_1)$")
    plt.plot(vs,f_p(vs), '--c', label="$f'(v_1)$")
    plt.scatter(v,f(v),color='r', edgecolor='k', zorder=5, label="Initial")
    v_2 = v - eta*f_p(v)
    plt.scatter(v_2,f(v_2), color='g', edgecolor='k', zorder=5, label="update")
    plt.plot([-5,4],[0,0],'k')
    
    plt.xlabel("$v_1$")
    plt.ylabel("$f(v_1)$")
    plt.legend()
    
    t_dir = -1 if f_p(v) > 0 else 1
    plt.text(v+(t_dir*1.5), f(v)+.2, "$-\eta\cdot f'(v_1)$", color='r')
    plt.annotate("", xy=(v, f(v)), xytext=(v_2, f(v)), color="r",
                arrowprops=dict(arrowstyle="<-", color="r"))
    
    plt.title("$\eta=%.2f$ $v_1=%.1f$, Richtung: %s" % (eta, v, dir_arrow[t_dir]))
    plt.ylim([-5,15])
    plt.xlim([-5.5,4.5])
    plt.tight_layout()
interactive_gradient_1d = lambda : interactive(gd, v=(-4.9,2.2,.1), eta=(0,1,0.01))