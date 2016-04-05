from colorrefinement.hopcraft import hopcraft
from graphs.basicgraphs import graph
from sortingalgorithms.mergesort import msintlist

"""
Methods for colorrefinement of graphs. Also can decide of graphs are isomorphic.
"""


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


def pruneandnumberisos(g):
    color = []
    index = []
    counted = []
    removed = []
    for vert in g.V():
        if len(color) > 0:
            for i in range(len(color)):
                if vert.colornum == color[i]:
                    g.V().remove(vert)
                    counted[i] += 1
                    if not removed[i]:
                        g.V().remove(index[i])
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
    return g, isocount


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
    max_color = g.maxcolornum()
    changedict = dict()
    i = 0
    while i <= max_color:
        v = g.getvwithcolornum(i)
        if len(v) > 1:
            changedict = herindeel(changedict, v)
        i += 1

    next_color = max_color + 1
    if changedict:
        keys = list(changedict.keys())
        for k in keys:
            vertices = changedict[k]
            for v in vertices:
                v.colornum = next_color
            next_color += 1

    if next_color != max_color + 1:
        g = refbynbs(g)
    return g


def herindeel(changedict, v):
    """
    Compares vertices with the same color values and differentiates them if they still turn out to be different by
    giving the vertices with the same value as the first checked vertex the original color and those that differentiate
    from the first checked vertex the next_color.
    :param v:
    :param changedict:
    :return g modified, next_color modified:
    """
    a = v[0].nbcolornums()
    msintlist(a)
    othernbs = list()
    i = 1
    while i < len(v):
        b = v[i].nbcolornums()
        msintlist(b)
        if a != b:
            othernbs.append(v[i])
        i += 1
    if othernbs:
        if changedict:
            maxkey = max(changedict.keys(), key=int)
            changedict[maxkey + 1] = othernbs
        else:
            changedict[0] = othernbs
    return changedict
