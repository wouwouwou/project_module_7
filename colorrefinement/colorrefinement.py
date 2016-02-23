from graphs import graphIO
from graphs import basicgraphs
from sortingalgorithms.mergesort import *

"""
INPUT: A graph G = (V, E), and initial coloring a0 of V
OUTPUT: A stable coloring ai of G.
"""


def isomorphicgraphs(graphlist):
    # get the colorings of the graphs in 1 list
    colorlist = []
    for g in graphlist:
        coloring = []
        for v in g:
            coloring.append(v.getcolornum())
        msintlist(coloring)
        colorlist.append(coloring)

    # loop over the list of colorings
    res = []
    i = 0
    while i < len(colorlist):
        colorcompare = [colorlist[i]]
        indexcompare = [i]
        j = i + 1
        while j < len(colorlist):
            if colorlist[i] == colorlist[j]:
                colorcompare.append(colorlist[j])
                indexcompare.append(j)
            j += 1
        if len(colorcompare) != 1:
            found = False
            for a in res:
                if colorcompare == a:
                    found = True
                    break
            if not found:
                res.append(indexcompare)
        i += 1
    return res


def colorrefinement(G):
    for v in G.V():
        v.setcolornum(v.deg() - 1)
    return checkneighbours(G)


def checkneighbours(g):
    max_color = g.maxcolornum()
    next_color = max_color + 1
    i = 1
    while i <= max_color:
        v = g.getvwithcolornum(i)
        if len(v) != 1:
            g, next_color = herindeel(g, v, next_color)
        i += 1
    if next_color != max_color + 1:
        g = checkneighbours(g)
    return g


def herindeel(g, v, next_color):
    a = v[0]
    na = a.nbcolornums()
    msintlist(na)
    changed = False
    i = 1
    while i < len(v):
        b = v[i]
        nb = b.nbcolornums()
        msintlist(nb)
        if na != nb:
            b.colornum = next_color
            changed = True
        i += 1
    if changed:
        next_color += 1
    return g, next_color
