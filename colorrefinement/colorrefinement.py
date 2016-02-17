from graphs import graphIO
from graphs import basicgraphs

"""
    INPUT: A graph G = (V, E), and initial coloring a0 of V
    OUTPUT: A stable coloring ai of G.
"""


def colorrefinement(G):
    for v in G.V():
        v.settag(v.deg() - 1)

    return checkneighbours(G)


def checkneighbours(g):
    max_color = g.maxtag()
    next_color = max_color + 1
    i = 1
    while i <= max_color:
        v = g.getVWithTag(i)
        if len(v) != 1:
            g, next_color = herindeel(g, v, next_color)
        i += 1
    if next_color != max_color + 1:
        g = checkneighbours(g)
    return g


def herindeel(g, v, next_color):
    a = v[0]
    na = a.neighbourtags()
    mergeSort(na)
    changed = False
    i = 1
    while i < len(v):
        b = v[i]
        nb = b.neighbourtags()
        mergeSort(nb)
        if na != nb:
            b.colornum = next_color
            changed = True
        i += 1
    if changed:
        next_color += 1
    return g, next_color


def mergeSort(a):
    if len(a) > 1:
        mid = len(a) // 2
        lefthalf = a[:mid]
        righthalf = a[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i = 0
        j = 0
        k = 0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                a[k] = lefthalf[i]
                i += 1
            else:
                a[k] = righthalf[j]
                j += 1
            k += 1

        while i < len(lefthalf):
            a[k] = lefthalf[i]
            i += 1
            k += 1

        while j < len(righthalf):
            a[k] = righthalf[j]
            j += 1
            k += 1
