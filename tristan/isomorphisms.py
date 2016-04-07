from graphs.basicgraphs import graph
from tristan.refinement import hopcroft

def isomorphisms(g1t, g2t, count=False):
    """
    Counts or determines the isomorphisms between two graphs.
    :param g1t: The first graph
    :param g2t: The second graph
    :param count: Count the amount of isomorphisms or determine only if there are isomorphisms.
    :return:
    """
    # Generate copies of the graphs to avoid pointer collision
    g1 = copygraph(g1t)
    g2 = copygraph(g2t)

    # Union graphs g1 and g2
    union = graph()
    union.createUnion(g1, g2)

    # Compute coarsest stable coloring that refines (g1, g2)
    hopcroft(union)

    # Generate color dictionaries
    g1colors = colordict(g1.V())
    g2colors = colordict(g2.V())
    ucolors = colordict(union)

    # Check if the graphs are balanced
    if not balanced(g1colors, g2colors):
        return 0

    # Check if the graphs define a bijection
    if bijection(g1colors, g2colors):
        return 1

    # Choose a color class with |C| >= 4. The first element fulfills.
    for cc in g1colors:
        if len(g1colors[cc]) > 1 and len(g2colors[cc]) > 1:
            colorclass = cc
            break
    x = g1colors[colorclass][0]

    # Determine the maxvalue in the color dictionary
    for i in range(len(g1colors)+1):
        if i not in g1colors:
            maxvalue = i
            break

    # Set the new colorclass of x.
    xoldcolornum = x.getcolornum()
    x.setcolornum(maxvalue)
    g1colors = colordict(copygraph(g1).V())

    # Count number of automorphisms
    num = 0

    # Loop all y in C & g2.V()
    for y in g2colors[colorclass]:
        # Set the new colorclass of y, preserve the old color class
        yoldcolornum = y.getcolornum()
        y.setcolornum(maxvalue)
        g2colors = colordict(g2.V())

        if count:
            # Count all automorphisms
            num = num + isomorphisms(g1, g2, count)
        else:
            # Only one automorphism fulfills
            return isomorphisms(g1, g2)

        # Reset the colornum of y
        y.setcolornum(yoldcolornum)
    # Reset the colornum of x
    x.setcolornum(xoldcolornum)

    # Return the number of automorphisms
    return num

def bijection(g1colors, g2colors):
    """
    Returns true if the colorings of graph g, graph h are equal

    :param g: graph g
    :param h: graph h
    :return: true if colorings of g and h are equal
    """
    try:
        for c in g1colors:
            if len(g1colors[c]) > 1 and len(g2colors[c]) == len(g1colors[c]):
                return False
    except KeyError:
        return False
    return True

def colordict(vlist):
    """
    Generate a colordictionary given a list of vertices
    :param vlist:
    :return:
    """
    result = dict()
    for v in vlist:
        if v.getcolornum() not in result:
            result[v.getcolornum()] = []
        result[v.getcolornum()].append(v)
    return result

def balanced(g1colors, g2colors):
    """
    Determine whether the graph is balanced
    :param g1colors:
    :param g2colors:
    :return:
    """
    try:
        if len(g1colors.keys()) != len(g2colors.keys()):
            return False
        for c in g1colors:
            if len(g1colors[c]) != len(g2colors[c]):
                return False
    except KeyError:
        return False
    return True

def copygraph(g):
    """
    Make a deepcopy of the graph.
    :param g: The graph to deepcopy
    :return:
    """
    f = graph(len(g.V()))
    for e in g.E():
        i = f.V()[e.tail().getlabel()]
        j = f.V()[e.head().getlabel()]
        f.addedge(i, j)

    for v in g.V():
        for u in f.V():
            if v.getlabel() == u.getlabel():
                u.setcolornum(v.getcolornum())
    return f
