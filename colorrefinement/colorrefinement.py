from graphs import graphIO
from graphs import basicgraphs
from sortingalgorithms.mergesort import *

"""
INPUT: A graph G = (V, E), and initial coloring a0 of V
OUTPUT: A stable coloring ai of G.
"""


def colorrefinement(G):
    for v in G.V():
        v.settag(v.deg() - 1)

    return checkneighbours(G)


def checkneighbours(g):
    max_color = g.maxcolornum()
    next_color = max_color + 1
    i = 1
    while i <= max_color:
        v = g.getvwithtag(i)
        if len(v) != 1:
            g, next_color = herindeel(g, v, next_color)
        i += 1
    if next_color != max_color + 1:
        g = checkneighbours(g)
    return g


def herindeel(g, v, next_color):
    a = v[0]
    na = a.neighbourtags()
    msintlist(na)
    changed = False
    i = 1
    while i < len(v):
        b = v[i]
        nb = b.neighbourtags()
        msintlist(nb)
        if na != nb:
            b.colornum = next_color
            changed = True
        i += 1
    if changed:
        next_color += 1
    return g, next_color
