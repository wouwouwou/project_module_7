from colorrefinement.hopcraft import hopcraft
from graphs.basicgraphs import graph
from sortingalgorithms.mergesort import msintlist

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


def colorrefinement(g):
    """
    Gives a stable coloring to graph g

    :param g: graph g
    :return: graph g with stable coloring
    """
    g.setcoloring(hopcraft(g))
    return g


def slowcolorrefinement(g):
    refbydeg(g)
    refbynbs(g)
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


def refbydeg(g):
    """
    Gives all the degrees a color value and gives the vertices the color according to their degree
    :param g:
    """
    if g.getcoloring():
        raise Exception("This graph already has a coloring!")
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
    if not g.getcolordict():
        raise Exception("This graph does not have a coloring yet. Add one!")
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
