from graphs import graphIO
from graphs import basicgraphs

"""
    INPUT: A graph G = (V, E), and initial coloring a0 of V
    OUTPUT: A stable coloring ai of G.
"""
def colorrefinement(G):
    for v in G.V():
        v.set_color_tag(v.deg())
    return G