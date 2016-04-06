from colorrefinement.hopcraft import hopcraft
from sortingalgorithms.mergesort import msintlist

"""
Methods for colorrefinement of graphs. Also can decide of graphs are isomorphic.
"""


def colorrefinegraphlist(graphlist):
    """
    Colorrefines every graph in the graphlist with hopcraft
    :param graphlist: The list of graphs to be colorrefined
    :return: A list of graphs which have a coarsest stable coloring
    """
    for g in graphlist:
        colorrefinement(g)
    return graphlist


def slowcolorrefinegraphlist(graphlist):
    """
    Colorrefines every graph in the graphlist with the slow algorithm
    :param graphlist: The list of graphs to be colorrefined
    :return: A list of graphs which have a coarsest stable coloring
    """
    for g in graphlist:
        slowcolorrefinement(g)
    return graphlist


def colorrefinement(g):
    """
    Gives a stable coloring to graph g with the hopcraft algorithm

    :param g: graph g
    :return: graph g with stable coloring
    """
    g.setcoloring(hopcraft(g))
    return g


def slowcolorrefinement(g):
    """
    Gives a stable coloring to graph g with a slow algorithm

    :param g: graph g
    :return: graph g with stable coloring
    """
    refbydeg(g)
    refbynbs(g)
    return g


def degreecoloring(g):
    """
    Gets the coloring based on the degree of the vertices of the graph
    :param g: graph g
    :return: coloring
    """
    coloring = dict()
    degtocol = g.degtocol()
    for v in g.V():
        colornum = degtocol.get(v.deg())

        if coloring.get(colornum) is None:
            coloring[colornum] = set()

        coloring[colornum].add(v)
    return coloring


def refbydeg(g):
    """
    Gives an initial coloring to the graph based on the degree of the vertices of the graph

    :param g: graph g
    :return: graph g with coloring based on degrees
    """
    if g.getcoloring():
        raise Exception("This graph already has a coloring!")
    coloring = degreecoloring(g)
    g.setcoloring(coloring)


def refbynbs(g):
    """
    Checks for every initially existing color if it has multiple vertices, if a color has multiple vertices it executes
    herindeel on that same colored group of vertices. When a change has been made during the execution of herindeel
    (indicated by the max_color value actually not being the max color anymore), refbynbs recurses untill no color
    changes were made during its run.

    :param g:
    :return g modified:
    """
    if not g.getcoloring():
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
            movevertices(g, changedict[k], next_color)
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


def movevertex(g, u, c):
    """
    Moves a single vertex from a color class to a new color class
    :param g: graph with the vertex
    :param u: vertex vertex to be moved
    :param c: current color class of the vertex
    :return: altered graph
    """
    coloring = g.getcoloring().copy()
    for v in g.V():
        if u.getlabel() == v.getlabel():
            u = v
            break
    coloring[c].remove(u)
    newc = max(coloring.keys()) + 1
    u.setcolornum(newc)
    setu = set()
    setu.add(u)
    coloring[newc] = setu
    g.setcoloring(coloring)
    return g


def movevertices(g, vcs, c):
    """
    Moves a group of vertices <vcs> in a graph <g> to a new color class <c>
    :param g: graph g
    :param vcs: the group of vertices
    :param c: the color class the group should have
    :return:
    """
    coloring = g.getcoloring().copy()
    if coloring[c] is None:
        coloring[c] = set()
    for v in vcs:
        coloring[v.getcolornum()].remove(v)
        v.setcolornum(c)
        coloring[c].add(v)
