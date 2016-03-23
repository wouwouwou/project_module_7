def isbalanced(g, h):
    """
    Returns true if the colorings of graph g, graph h are equal

    :param g: graph g
    :param h: graph h
    :return: true if colorings of g and h are equal
    """
    cg = g.getcoloring()
    ch = h.getcoloring()
    if len(list(cg.keys())) != len(list(ch.keys())):
        return False
    for c in cg:
        if len(cg[c]) != len(ch[c]):
            return False
    return True


def definesbijection(g, h):
    """
    Return true if graph g and graph h define a bijection

    :param g: graph g
    :param h: graph h
    :return: tru if g and h define a bijection
    """
    if not isbalanced(g, h):
        return False
    cg = g.getcoloring()
    ch = h.getcoloring()
    for c in cg:
        if len(cg[c]) != 1 and len(ch[c]) != 1:
            return False
    return True


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


def processgraphlist(graphlist):
    # todo      question: do single graphs have to be included? Do we have to get the number of
    # todo      automorphisms from this graph to itself?
    res = dict()
    graphdict = dict()
    i = 0
    while i < len(graphlist):
        graphdict[i] = graphlist[i]
        i += 1
    while len(graphdict) != 0:
        graphdict, isogroup, aut = processing(graphdict)
        res[isogroup] = aut

    # prints to standardout the isogroup and #aut in that group
    for isogroup in list(res.keys()):
        print(str(isogroup) + " " + str(res[isogroup]) + "\n")


def processing(graphdict):
    indexlist = list(graphdict.keys())
    minindex = min(indexlist)
    g = graphdict[minindex]
    nextdict = dict()
    isogroup = [minindex]
    aut = -1
    i = 1
    while i < len(indexlist):
        graphindex = indexlist[i]
        graph = graphdict[graphindex]

        if aut == -1:
            isomorph, aut = processgraphs(g, graph)
        else:
            isomorph = isisomorphic(g, graph)

        if isomorph:
            isogroup.append(graphindex)
        else:
            nextdict[graphindex] = graph

        i += 1

    return nextdict, isogroup, aut


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


def countautomorphisms(g):
    """
    Counts automorphisms of a graph. Should return 1 <= n <= n! where n is amount of vertices en the graph
    :param g:
    :return:
    """
    # todo implement this again
    pass
