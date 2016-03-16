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
    if cg.len() != ch.len():
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


def countautomorphisms(g):
    """
    Counts automorphisms of a graph. Should return 1 <= n <= n! where n is amount of vertices en the graph
    :param g:
    :return:
    """
    # todo implement this again
    pass
