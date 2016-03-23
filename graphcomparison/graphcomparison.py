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
        isomorph = False

        # if aut == -1 then we have to test all the conditions.
        if aut == -1:
            if definesbijection(g, graph):
                isomorph = True
                aut = 1
            elif not isbalanced(g, graph):
                pass
            else:
                aut = countautomorphisms(g, graph)
                isomorph = True

        # if aut == 1 we only have to check if the graphs define a bijection
        elif aut == 1:
            if definesbijection(g, graph):
                isomorph = True

        # if aut > 1 we have to branch, but only to check if the graphs are isomorphic
        elif aut > 1:
            isomorph = isomorphicbranching(g, graph)

        # another value for aut is not accepted!
        else:
            raise Exception("aut is not valid!")

        if isomorph:
            isogroup.append(graphindex)
        else:
            nextdict[graphindex] = graph

        i += 1

    return nextdict, isogroup, aut


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


def countautomorphisms(g):
    """
    Counts automorphisms of a graph. Should return 1 <= n <= n! where n is amount of vertices en the graph
    :param g:
    :return:
    """
    # todo implement this again
    pass
