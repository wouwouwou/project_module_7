from graphs import graphIO
from graphs import basicgraphs
from sortingalgorithms.mergesort import *
from graphs.basicgraphs import graph
from graphcomparison.graphcomparison import *

"""
Methods for colorrefinement of graphs. Also can decide of graphs are isomorphic.
"""


def disjointunion(g: graph, h: graph):
    """
    Create a disjoint union of two graphs.
    :param g: The first graph
    :param h: The second graph
    :return: The two graphs combined
    """
    f = graph(len(g.V()) + len(h.V()))
    combinedlist = g.V() + h.V()
    for i in range(len(combinedlist)):
        v = combinedlist[i]
        for e in v.getinclist():
            if e.tail() == v:
                f.addedge(f[i], f[combinedlist.index(e.head())])

    colorrefinement(f)
    return f

def getcoloringdict(V):
    resultdict = dict()
    maximum = 0
    for v in V:
        if resultdict.get(v.getcolornum()) is None:
            resultdict[v.getcolornum()] = set()
        resultdict[v.getcolornum()].add(v)
        maximum = max(maximum, v.getcolornum())
    return resultdict, maximum

def countiso(g, h):
    colorrefinement(g)
    colorrefinement(h)
    return countisomorphism(g.V(), h.V())

def countisomorphism(d, i):
    """
    Compute the coarsest steble coloring Beta that refines alpha(.V(), i.V())
    :param d:graph
    :param i:graph
    :return:
    """
    # Refine both graphs prior processing // Reported working.

    # If Beta is unbalanced // Reported working.
    if not isbalancedvertex(d, i):
        return 0

    # If Beta defines a bijection
    if definesbijectionvertex(d, i):
        return 1


    coloringdictD, maxD = getcoloringdict(d)
    coloringdictI, maxI = getcoloringdict(i)

    possibleclasses = set()
    for c in coloringdictD:
        if len(coloringdictD[c]) >= 2 and len(coloringdictI[c]) >= 2:
            possibleclasses.add(c)

    for a in possibleclasses:
        b = a
        break


    for u in d:
        if u.getcolornum() == b:
            v = u

    num = 0
    # Temporally set color num
    if possibleclasses.__contains__(v.getcolornum()):
        vold = v.getcolornum()
        v.setcolornum(maxD + 2)
        for u in i:
            if possibleclasses.__contains__(u.getcolornum()):
                # Temporally set colornum
                uold = u.getcolornum()
                u.setcolornum(maxI + 2)
                num += countisomorphism(d, i)
                u.setcolornum(uold)
        v.setcolornum(vold)
    return num


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
        print(msintlist(graphdict[i].getcoloring()))
        i += 1
    while len(graphdict) != 0:
        graphdict, isogroup = iteration(graphdict)
        if len(isogroup) > 1:
            res.append(isogroup)
    return res


def iteration(graphdict):
    """
    Creates and returns an array nextlist which contains the ___ and an array isogroup which contains the color codes of
    ___
    :param graphdict:
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
    return nextdict, isogroup

def getcoloringvertex(V):
    """
    Returns a sorted coloring of vertices v
    :param v: vertices v
    :return: sorted coloring of vertices v
    """
    coloring = []
    for v in V:
        coloring.append(v.getcolornum())
    msintlist(coloring)
    return coloring


def isbalancedvertex(v, v1):
    """
    Returns true if the colorings of vertices v, vertices v1 are equal.
    :param v: vertices
    :param v1: vertices
    :return: true if colorings of v and v1 are equal
    """
    cv = getcoloringvertex(v)
    cv1 = getcoloringvertex(v1)
    return cv == cv1


def definesbijectionvertex(v, v1):

    if isbalancedvertex(v, v1):
        i = 0
        cv = getcoloringvertex(v)
        while i < len(cv) - 1:
            if cv[i] == cv[i+1]:
                return False
            i += 1
        return True
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
    unique_color = set()
    max_color = g.maxcolornum()
    next_color = max_color + 1
    i = 0
    while i <= max_color:
        if i not in unique_color:
            v = g.getvwithcolornum(i)
            if len(v) == 1:
                unique_color.add(i)
            elif len(v) > 1:
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
    a = v[0].nbcolornums()
    msintlist(a)
    changed = False
    i = 1
    while i < len(v):
        b = v[i].nbcolornums()
        msintlist(b)
        if a != b:
            v[i].colornum = next_color
            changed = True
        i += 1
    if changed:
        next_color += 1
    return g, next_color

def deepcopy(obj):
    if isinstance(obj, dict):
        return {deepcopy(key): deepcopy(value) for key, value in obj.items()}
    if hasattr(obj, '__iter__'):
        return type(obj)(deepcopy(item) for item in obj)
    return obj


def pruneandnumberisos(G):
    color = []
    index = []
    counted = []
    removed = []
    for vert in G.V():
        if len(color) > 0:
            for i in range(len(color)):
                if vert.colornum == color[i]:
                    G.V().remove(vert)
                    counted[i] += 1
                    if not removed[i]:
                        G.V().remove(index[i])
                        removed[i] = True
                else:
                    color.append(vert.colornum)
                    index.append(vert)
                    removed.append(False)
                    counted.append(1)
        else:
            color.append(vert.colornum)
            index.append(vert)
            removed.append(False)
            counted.append(1)
    isocount = 1
    for mult in counted:
        isocount *= mult
    return G, isocount

