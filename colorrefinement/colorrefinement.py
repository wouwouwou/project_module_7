from colorrefinement.hopcraft import hopcraft
from graphcomparison.graphcomparison import *

"""
Methods for colorrefinement of graphs. Also can decide of graphs are isomorphic.
"""


def definesbijectionvertex(v, v1):
    if isbalancedvertex(v, v1):
        i = 0
        cv = getcoloringvertex(v)
        while i < len(cv) - 1:
            if cv[i] == cv[i + 1]:
                return False
            i += 1
        return True
    return False


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


def getcoloringvertex(v):
    """
     Returns a sorted coloring of vertices v
     :param v: vertices v
     :return: sorted coloring of vertices v
    """
    coloring = []
    for v in v:
        coloring.append(v.getcolornum())
    msintlist(coloring)
    return coloring


def disjointuniongraphs(g: graph, h: graph):
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


def disjointunionvertices(d, i):
    f = graph(len(d) + len(i))
    combinedlist = d + i
    for i in range(len(combinedlist)):
        v = combinedlist[i]
        for e in v.getinclist():
            if e.tail() == v:
                f.addedge(f[i], f[combinedlist.index(e.head())])

    colorrefinement(f)
    return f


def getcoloringdict(v):
    resultdict = dict()
    maximum = 0
    for v in v:
        if resultdict.get(v.getcolornum()) is None:
            resultdict[v.getcolornum()] = set()
        resultdict[v.getcolornum()].add(v)
        maximum = max(maximum, v.getcolornum())
    return resultdict, maximum


def countiso(g, h):
    colorrefinement(g)
    colorrefinement(h)
    return countisomorphism(g.V(), h.V())


def makegraphfromvertices(d):
    g = graph(len(d))
    for i in range(len(d)):
        v = d[i]
        g.V()[i].setcolornum(d[i].getcolornum())
        for e in v.getinclist():
            if e.tail() == v:
                g.addedge(g[i], g[d.index(e.head())])

    colorrefinement(g)

    return g


def countisomorphism(d, i):
    """
     Compute the coarsest stable coloring Beta that refines alpha(g.V(), h.V())
     :param d: vertices of graph g
     :param i: vertices of graph h
     :return:
     """
    # Refine both graphs prior processing // Reported working.
    s = d[:]
    t = i[:]
    g = makegraphfromvertices(s)
    h = makegraphfromvertices(t)

    q = g.getcoloring()
    msintlist(q)
    print(q)
    q = h.getcoloring()
    msintlist(q)
    print(q)

    # If Beta is unbalanced // Reported working.
    if not isbalanced(g, h):
        return 0

    # If Beta defines a bijection
    if definesbijection(g, h):
        return 1

    coloringdictg = g.getcolordict()
    coloringdictt = h.getcolordict()

    possibleclasses = set()
    for c in coloringdictg:
        if len(coloringdictg[c]) >= 2 and len(coloringdictt[c]) >= 2:
            possibleclasses.add(c)

    for a in possibleclasses:
        b = a
        break

    for u in s:
        if u.getcolornum() == b:
            x = u
        if x == u:
            break

    num = 0
    if possibleclasses.__contains__(x.getcolornum()):
        xold = x.getcolornum()
        x.setcolornum(g.maxcolornum() + 1)
        for y in t:
            if possibleclasses.__contains__(y.getcolornum()):
                # Temporally set colornum
                yold = y.getcolornum()
                y.setcolornum(h.maxcolornum() + 1)
                num += countisomorphism(s, t)
                y.setcolornum(yold)
        x.setcolornum(xold)
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
        c = graphdict[i].getcoloring()
        msintlist(c)
        print(c)
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


def colorrefinement(g):
    """
    Gives a stable coloring to graph g

    :param g: graph g
    :return: graph g with stable coloring
    """
    g.setcoloring(hopcraft(g))
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


"""
def deepcopy(obj):
    if isinstance(obj, dict):
        return {deepcopy(key): deepcopy(value) for key, value in obj.items()}
    if hasattr(obj, '__iter__'):
        return type(obj)(deepcopy(item) for item in obj)
    return obj
"""


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
