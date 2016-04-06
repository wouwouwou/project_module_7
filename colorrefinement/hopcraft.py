import unittest

from graphs.graphIO import loadgraph, writeDOT
import time
from graphs.basicgraphs import graph

def neighbourlist(g: graph, directed=False):
    """
     Generate an incoming list for given vertices.
     Set directed to True if the graph is directed.
     :param directed:
     :param g:
    """
    result = dict()
    for v in g.V():
        result[v] = set()
    for e in g.E():
        result[e.tail()].add(e.head())
        if not directed:
            result[e.head()].add(e.tail())
    return result

def generatePfromColors(G):
    p = []
    colors = dict()
    for v in G.V():
        if v.colornum in colors.keys():
            colors[v.colornum].add(v)
        else:
            colors[v.colornum] = {v}
    keys = list(colors.keys())
    for key in keys:
        p.append(colors[key])
    return p

def writeColors(partitions):
    for i in range(len(partitions)):
        for v in partitions[i]:
            v.colornum = i

def hopcraft(g: graph, usecolors=False):
    """
     Generate a Minimum DFA as described by the Hopcroft's algorithm
     This algorithm has a worst-case complexity of O(ns log n), with n the number of states and s the different amount of degrees.
     @see https://en.wikipedia.org/wiki/DFA_minimization#Hopcroft.27s_algorithm
     @see https://riunet.upv.es/bitstream/handle/10251/27623/partial%20rev%20determ.pdf?sequence=1 Algorithm 6.1
     :param smallestpartition: Select the smallest partition to refine first.
     :param g: The graph
    """

    neighbours = neighbourlist(g, g.isdirected())
    p = []
    pSplit = []
    degrees = dict()
    if g.getcoloring():
        degrees = g.getcoloring()
    else:
        for v in g.V():
            degree = len(neighbours[v])
            if degrees.get(degree, -1) == -1:
                degrees[degree] = {v}
            else:
                degrees[degree].add(v)

    if usecolors:
        p = generatePfromColors(g)
        pSplit = generatePfromColors(g)
    else:
        for k in degrees:
            p.append(degrees[k])
            pSplit.append(degrees[k])

    w = set(range(len(p)))
    # Loop queue
    while w:
        # Choose and remove a set A from W
        aN = w.pop()
        a = p[aN]
        nbs = set()
        for va in a:
            nbs |= neighbours[va]

        # Iterate for each degree in degrees
        for color in pSplit:
            # Let X be the set of states for which a transition on degree leads to a state in A
            x = nbs & color
            if x:
                # Iterate for each c in range(len(p)), with x&y and y-x not empty.
                for yN in range(len(p)):
                    if len(p[yN]) > 1:
                        # Replace y in p by the two sets x&y and y-x
                        y = p[yN]
                        both = x & y
                        ynotx = y - x
                        if both and ynotx:

                            p[yN] = both
                            p.append(ynotx)
                            # If y is in w
                            if yN in w:
                                # Add position of p.add(y - x) to w
                                w.add(len(p) - 1)
                            else:
                                # Partition the smallest one.
                                if len(both) <= len(ynotx):
                                    # Add position of x&y in p to w
                                    w.add(yN)
                                else:
                                    # Add position of y-x in p to w
                                    w.add(len(p) - 1)
    r = dict()
    count = 0
    for ap in p:
        r[count] = ap
        count += 1
    return r



def fastautomorphismcount(g: graph):
    """
    Calculate the amount of automorphisms of one graph.
    :param g:
    :return:
    """
    coloring = hopcraft(g, False)
    isomorphisms = 1
    for cl in range(len(coloring)):
        isomorphisms *= len(coloring[cl])
    return isomorphisms


class TestColorRefinement(unittest.TestCase):
    def testIsomorphismCount(self):
        start = time.time()

        # Load a Python tuple of length 2, where the first element is a list of Graphs.
        # l = loadgraph('../test_grafen/colorref_smallexample_2_49.grl', readlist=True)
        #l = loadgraph('../test_grafen/colorref_smallexample_2_49.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_4_16.grl', readlist=True)
        l = loadgraph('../test_grafen/colorref_smallexample_4_7.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_6_15.grl', readlist=True)
        # l = loadgraph('../test_grafen/threepaths10240.gr', readlist=True)
        #   `l = loadgraph('../test_grafen/torus24.grl', readlist=True)
        # l = loadgraph('../test_grafen/trees90.grl', readlist=True)
        # Gets the first graph out of the list of graphs
        graph = fasthopcraft(l[0][1])

        end = time.time()
        t = end - start
        writeDOT(graph, "output.dot")
        print("Execution time: " + str(t))


if __name__ == '__main__':
    unittest.main()
