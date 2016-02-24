from graphs import graphIO
from graphs import basicgraphs
from sortingalgorithms.mergesort import *
from graphs.basicgraphs import graph

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
    print(g.V())
    return countisomorphism(g.V(), h.V(), True)

def countisomorphism(d, i, first):
    """
    Compute the coarsest steble coloring Beta that refines alpha(.V(), i.V())
    :param d:graph
    :param i:graph
    :return:
    """
    # Refine both graphs prior processing // Reported working.

    # If Beta is unbalanced // Reported working.
    if not isbalancedvertex(d, i):
        print("Unbalanced!")
        return 0

    # If Beta defines a bijection
    if definesbijectionvertex(d, i):
        print("Bijection")
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
                num += countisomorphism(d, i, False)
                u.setcolornum(uold)
        v.setcolornum(vold)
    if first:
        print(num)
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
        i += 1
    while len(graphdict) != 0:
        graphdict, isogroup = iteration(graphdict)
        if len(isogroup) > 1:
            res.append(isogroup)
    return res


def iteration(graphdict):
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
            isogroup.append(i)
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

    It temporarily can return None if graph g and graph h are balanced but not define a bijection

    :param g: graph g
    :param h: graph h
    :return: true if g and h are isomorphic
    """
    if not isbalanced(g, h):
        return False
    elif definesbijection(g, h):
        return True
    return basicgraphs.GraphError("Balanced but not bijection!")


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
    degs = g.degset()
    degcol = dict()
    i = 0
    for d in degs:
        degcol[d] = i
        i += 1
    for v in g.V():
        v.setcolornum(degcol.get(v.deg()))


def refbynbs(g):
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

def deepcopy(obj):
    if isinstance(obj, dict):
        return {deepcopy(key): deepcopy(value) for key, value in obj.items()}
    if hasattr(obj, '__iter__'):
        return type(obj)(deepcopy(item) for item in obj)
    return obj