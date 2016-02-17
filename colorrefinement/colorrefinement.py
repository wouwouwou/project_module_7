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


def checkneighbours(g):
    """
    max_color = g.get_max_color()
    next_color = max_color + 1
    i = 1
    while i <= max_color:
        v = g.get_nodes_color_i(i)
        if len(v) != 1:
            g, nextcolor = herindeel(g, v, next_color)
        i++

    """
    for v in g.V():
        pass
    pass


def herindeel(g, v, next_color):
    """
    a = v[0]
    na = a.get_neighbour_colors()
    differs = list()
    changed = False
    i = 1
    while i < len(v):
        b = v[i]
        nb = b.get_neighbour_colors()
        if nb != na:
            b.tag = next_color
            changed = True
    if changed:
        next_color += 1
    return g, next_color
    """
    pass