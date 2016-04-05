from colorrefinement.colorrefinement import colorrefinement, slowcolorrefinement, refbynbs
from graphs.basicgraphs import graph
from graphs.graphIO import writeDOT
from sortingalgorithms.mergesort import msintlist


def processgraphlist(graphlist):
    for g in graphlist:
            colorrefinement(g)
    res = list()
    graphdict = dict()
    i = 0
    while i < len(graphlist):
        graphdict[i] = graphlist[i]
        i += 1
    while len(graphdict) != 0:
        graphdict, isogroup, aut = processing(graphdict)
        res.append((isogroup, aut))

    # prints to standardout the isogroup and #aut in that group
    for tup in res:
        print(tup)


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
                isomorph = isomorphicbranching(g, graph)
                if isomorph:
                    aut = countautomorphisms(g, graph)
                if aut == 0:
                    aut = -1

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


def isbalancedslow(g, h):
    cg = g.getslowcoloring()
    ch = h.getslowcoloring()
    msintlist(cg)
    msintlist(ch)
    if cg == ch:
        return True
    if max(cg) != max(ch):
        return False
    i = 0
    dif = 0
    while i <= max(cg):
        s = len(g.getvwithcolornum(i))
        t = len(h.getvwithcolornum(i))
        dif += (s-t)
        i += 1
    return dif == 0

    return cg == ch


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


def definesbijectionslow(g, h):
    if isbalancedslow(g, h):
        i = 0
        cg = g.getslowcoloring()
        msintlist(cg)
        while i < len(cg) - 1:
            if cg[i] == cg[i + 1]:
                return False
            i += 1
        return True
    return False


def countautomorphisms(g, graph):
    """
    Counts automorphisms of a graph. Should return 1 <= n <= n! where n is amount of vertices en the graph
    :param graph:
    :param g:
    :return:
    """
    # Refine both graphs prior processing // Reported working.
    g = colorrefinement(g)
    graph = colorrefinement(graph)
    g = colorrefinement(g)
    graph = colorrefinement(graph)

    # If Beta is unbalanced // Reported working.
    if not isbalanced(g, graph):
        return 0

    # If Beta defines a bijection
    if definesbijection(g, graph):
        return 1

    # choose a coloring class which contains more than 2 vertices
    coloringg = g.getcoloring()
    coloringgraph = graph.getcoloring()

    possibleclasses = list()

    for c in coloringg.keys():
        if len(coloringg[c]) == len(coloringgraph[c]) and len(coloringg[c]) > 1:
            possibleclasses.append(c)

    if len(possibleclasses) == 0:
        raise Exception("No possible classes!")

    a = possibleclasses[0]

    # choose a vertex in the chosen coloring class and in V(g)
    x = None

    for v in coloringg[a]:
        x = v
        break

    if x is None:
        raise Exception("failed to choose a vertex in the chosen color class")

    num = 0
    s = copygraph(g)
    colorings = s.getcoloring().copy()
    for v in s.V():
        if x.getlabel() == v.getlabel():
            x = v
            break
    colorings[a].remove(x)
    nextclass = max(colorings.keys()) + 1
    setx = set()
    setx.add(x)
    colorings[nextclass] = setx
    s.setcoloring(colorings)

    # for each vertex in V(graph) with the same colorgraph
    for y in coloringgraph[a]:
        t = copygraph(graph)
        coloringt = t.getcoloring().copy()
        for v in t.V():
            if y.getlabel() == v.getlabel():
                y = v
                break
        coloringt[a].remove(y)
        nextclass = max(coloringt.keys()) + 1
        sety = set()
        sety.add(y)
        coloringt[nextclass] = sety
        t.setcoloring(coloringt)
        num += countautomorphisms(s, t)

    return num


def slowcountautomorphisms(g, graph):
    """
    Counts automorphisms of a graph. Should return 1 <= n <= n! where n is amount of vertices en the graph
    :param graph:
    :param g:
    :return:
    """

    # Refine both graphs prior processing // Reported working.
    g = refbynbs(g)
    graph = refbynbs(graph)

    print(g.getcolordict())
    print(graph.getcolordict())

    # If Beta is unbalanced // Reported working.
    if not isbalancedslow(g, graph):
        print("+0")
        return 0

    # If Beta defines a bijection
    if definesbijectionslow(g, graph):
        print("+1")
        return 1

    # choose a coloring class which contains more than 2 vertices
    coloringg = g.getcolordict()
    coloringgraph = graph.getcolordict()

    possibleclasses = list()

    for c in coloringg.keys():
        if len(coloringg[c]) == len(coloringgraph[c]) and len(coloringg[c]) > 1:
            possibleclasses.append(c)

    if len(possibleclasses) == 0:
        raise Exception("No possible classes!")

    a = possibleclasses[0]

    # choose a vertex in the chosen coloring class and in V(g)
    x = None

    for v in coloringg[a]:
        x = v
        break

    if x is None:
        raise Exception("failed to choose a vertex in the chosen color class")

    num = 0
    s = slowcopygraph(g)
    for v in s.V():
        if x.getlabel() == v.getlabel():
            x = v
            break
    x.colornum = s.maxcolornum() + 1

    # for each vertex in V(graph) with the same colorgraph
    for y in coloringgraph[a]:
        t = slowcopygraph(graph)
        for v in t.V():
            if y.getlabel() == v.getlabel():
                y = v
                break
        y.colornum = t.maxcolornum() + 1
        num += slowcountautomorphisms(s, t)
    return num


def isomorphicbranching(g, graph):
    """
    Individualisation branching for determining if the graphs are isomorphic
    :param graph:
    :param g:
    :return:
    """
    # Refine both graphs prior processing // Reported working.
    g = colorrefinement(g)
    graph = colorrefinement(graph)
    g = colorrefinement(g)
    graph = colorrefinement(graph)

    # If Beta is unbalanced // Reported working.
    if not isbalanced(g, graph):
        return False

    # If Beta defines a bijection
    if definesbijection(g, graph):
        return True

    # choose a coloring class which contains more than 2 vertices
    coloringg = g.getcoloring()
    coloringgraph = graph.getcoloring()

    possibleclasses = list()

    for c in coloringg.keys():
        if len(coloringg[c]) == len(coloringgraph[c]) and len(coloringg[c]) > 1:
            possibleclasses.append(c)

    if len(possibleclasses) == 0:
        raise Exception("No possible classes!")

    a = possibleclasses[0]

    # choose a vertex in the chosen coloring class and in V(g)
    x = None

    for v in coloringg[a]:
        x = v
        break

    if x is None:
        raise Exception("failed to choose a vertex in the chosen color class")

    num = False
    s = copygraph(g)
    colorings = s.getcoloring().copy()
    for v in s.V():
        if x.getlabel() == v.getlabel():
            x = v
            break
    colorings[a].remove(x)
    nextclass = max(colorings.keys()) + 1
    setx = set()
    setx.add(x)
    colorings[nextclass] = setx
    s.setcoloring(colorings)

    # for each vertex in V(graph) with the same colorgraph
    for y in coloringgraph[a]:
        t = copygraph(graph)
        coloringt = t.getcoloring().copy()
        for v in t.V():
            if y.getlabel() == v.getlabel():
                y = v
                break
        coloringt[a].remove(y)
        nextclass = max(coloringt.keys()) + 1
        sety = set()
        sety.add(y)
        coloringt[nextclass] = sety
        t.setcoloring(coloringt)
        num = isomorphicbranching(s, t)
        if num:
            break

    return num


def copygraph(g):
    f = graph(len(g.V()))
    for e in g.E():
        i = f.V()[e.tail().getlabel()]
        j = f.V()[e.head().getlabel()]
        f.addedge(i, j)

    coloring = g.getcoloring().copy()
    resdict = dict()
    for key in coloring.keys():
        resset = set()
        for u in coloring[key]:
            for v in f.V():
                # todo more effectively search for the same label!
                if u.getlabel() == v.getlabel():
                    resset.add(v)
                    break
        resdict[key] = resset
    f.setcoloring(resdict)
    return f


def slowcopygraph(g):
    f = graph(len(g.V()))
    for e in g.E():
        i = f.V()[e.tail().getlabel()]
        j = f.V()[e.head().getlabel()]
        f.addedge(i, j)

    for u in g.V():
        for v in f.V():
            if u.getlabel() == v.getlabel():
                v.colornum = u.colornum
    return f


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
