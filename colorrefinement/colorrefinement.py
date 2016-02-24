from graphs import graphIO
from graphs import basicgraphs
from sortingalgorithms.mergesort import *

"""
Methods for colorrefinement of graphs. Also can decide of graphs are isomorphic.
"""


def isomorphicgraphs(graphlist):
    """
    Return a list of the indices of the graphs which are isomorphic to each other

    :param graphlist: a list of graphs
    :return: a list of indices of the graphs which are isomorphic to each other
    """
    res = []
    graphdict = dict()
    i = 0
    while i < len(graphlist):
        graphdict[i] = graphlist[i]
        print(getcoloring(graphdict[i]))
        i += 1
    while len(graphdict) != 0:
        graphdict, isogroup = iteration(graphdict)
        if len(isogroup) > 1:
            res.append(isogroup)
    return res


def iteration(graphlist):
    """
    Creates and returns an array nextlist which contains the ___ and an array isogroup which contains the color codes of
    ___
    :param graphlist:
    :return:
    """
    indexlist = list(graphdict.keys())
    minindex = min(indexlist)
    g = graphdict[minindex]
    nextdict = dict()
    isogroup = [minindex]
    i = 1
    while i < len(indexlist):
        graphindex = indexlist[i]
        graph = graphdict[graphindex]
        if isomorphic(g, graph):
            isogroup.append(graphindex)
        else:
            nextdict[graphindex] = graph
        i += 1
    return nextlist, isogroup


def getcoloring(g):
    """
    Returns a sorted coloring of graph g

    :param g: graph g
    :return: sorted coloring of graph g
    """
    coloring = []
    for v in g:
        coloring.append(v.getcolornum())
    msintlist(coloring)
    return coloring


def isbalanced(g, h):
    """
    Returns true if the colorings of graph g, graph h are equal

    :param g: graph g
    :param h: graph h
    :return: true if colorings of g and h are equal
    """
    cg = getcoloring(g)
    ch = getcoloring(h)
    return cg == ch


def definesbijection(g, h):
    """
    Return true if graph g and graph h define a bijection

    :param g: graph g
    :param h: graph h
    :return: tru if g and h define a bijection
    """
    if isbalanced(g, h):
        i = 0
        cg = getcoloring(g)
        while i < len(cg) - 1:
            if cg[i] == cg[i+1]:
                return False
            i += 1
        return True
    return False


def isomorphic(g, h):
    """
    Returns true if graph g and graph h are isomorphic

    It temporarily returns False if graph g and graph h are balanced but not define a bijection

    :param g: graph g
    :param h: graph h
    :return: true if g and h are isomorphic
    """
    if not isbalanced(g, h):
        return False
    elif definesbijection(g, h):
        return True
    # todo: return something else when balanced but not bijection!
    return False


def colorrefinement(g):
    """
    Gives a stable coloring to graph g

    :param g: graph g
    :return: graph g with stable coloring
    """
    refbydeg(g)
    refbynbs(g)
    return g


def refbydeg(g):
    """
    Gives all the degrees a color value and gives the vertices the color according to their degree
    :param g:
    """
    degs = g.degset()
    degcol = dict()
    i = 0
    for d in degs:
        degcol[d] = i
        i += 1
    for v in g.V():
        v.setcolornum(degcol.get(v.deg()))


def refbynbs(g):
    """
    Checks for every initially existing color if it has multiple vertices, if a color has multiple vertices it executes
    herindeel on that same colored group of vertices. When a change has been made during the execution of herindeel
    (indicated by the max_color value actually not being the max color anymore), refbynbs recurses untill no color
    changes were made during its run.
    :param g:
    :return g modified:
    """
    max_color = g.maxcolornum()
    next_color = max_color + 1
    i = 0
    while i <= max_color:
        v = g.getvwithcolornum(i)
        if len(v) > 1:
            g, next_color = herindeel(g, v, next_color)
        i += 1
    if next_color != max_color + 1:
        g = refbynbs(g)
    return g


def herindeel(g, v, next_color):
    """
    Compares vertices with the same color values and differentiates them if they still turn out to be different by
    giving the vertices with the same value as the first checked vertex the original color and those that differentiate
    from the first checked vertex the next_color.
    :param g:
    :param v:
    :param next_color:
    :return g modified, next_color modified:
    """
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
