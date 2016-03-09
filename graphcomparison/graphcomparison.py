from graphs import graphIO
from graphs import basicgraphs
from sortingalgorithms.mergesort import *
from graphs.basicgraphs import *
from colorrefinement import *
from colorrefinement.colorrefinement import *


def isbalanced(g, h):
    """
    Returns true if the colorings of graph g, graph h are equal

    :param g: graph g
    :param h: graph h
    :return: true if colorings of g and h are equal
    """
    cg = g.getcoloring()
    ch = h.getcoloring()
    msintlist(cg)
    msintlist(ch)
    return cg == ch


def definesbijection(g, h):
    """
    Return true if graph g and graph h define a bijection

    :param g: graph g
    :param h: graph h
    :return: tru if g and h define a bijection
    """
    if isbalanced(g, h):
        i = 0
        cg = g.getcoloring()
        msintlist(cg)
        while i < len(cg) - 1:
            if cg[i] == cg[i+1]:
                return False
            i += 1
        return True
    return False


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
