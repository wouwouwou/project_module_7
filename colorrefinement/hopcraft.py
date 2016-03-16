import unittest
from graphs.graphIO import loadgraph
import time
from graphs.basicgraphs import graph

"""
    Generate an incoming list for given vertices.
    Set directed to True if the graph is directed.
"""
def neighbourlist(g: graph, directed=False):
    result = dict()
    for v in g.V():
        result[v] = set()
    for e in g.E():
        result[e.tail()].add(e.head())
        if not directed:
            result[e.head()].add(e.tail())
    return result

"""
    Generate a Minimum DFA as described by the Hopcroft's algorithm
    @see https://en.wikipedia.org/wiki/DFA_minimization#Hopcroft.27s_algorithm
"""
def hopcraft(g: graph):
    neighbours = neighbourlist(g, g.isdirected())

    degrees = dict()
    p = []

    # degrees := {1: p1, 2: p2, ..., n: pn} met px = {v1, v2, ..., vk}
    for v in g.V():
        degree = len(neighbours[v])
        if degree not in degrees.keys():
            degrees[degree] = set()
        degrees[degree].add(v)

    # p := {p1, p2, ..., pn}
    for k in degrees:
        p.append(degrees[k])

    # W := {p1}
    w = {0}
    while w:
        # Choose and remove a set A from W
        aN = w.pop()
        a = p[aN]

        # Iterate for each degree in degrees
        for degree in degrees:

            # Let X be the set of states for which a transition on degree leads to a state in A
            nbs = set()
            for v in a:
                nbs |= neighbours[v]
            x = nbs | degrees[degree]

            # Iterate for each c in range(len(p)), with x&y and y-x not empty.
            for yN in {c for c in range(len(p)) if x & p[c] and p[c] - x}:
                # Replace y in p by the two sets x&y and y-x
                y = p[yN]
                p[yN] = x & y
                p.append(y - x)

                # If y is in w
                if yN in w:
                    # Add position of p.add(y - x) to w
                    w.add(len(p) - 1)
                else:
                    # Partition the smallest one.
                    if len(x & y) <= len(y - x):
                        # Add position of x&y in p to w
                        w.add(yN)
                    else:
                        # Add position of y-x in p to w
                        w.add(len(p) - 1)
    coloring = dict()
    for pN in range(len(p)):
        coloring[pN] = p[pN]

    print(coloring)
    return coloring



class TestColorRefinement(unittest.TestCase):
    def testIsomorphismCount(self):
        start = time.time()

        # Load a Python tuple of length 2, where the first element is a list of Graphs.
        l = loadgraph('../test_grafen/colorref_smallexample_2_49.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_4_7.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_4_16.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_6_15.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_largeexample_4_1026.grl', readlist=True)
        # Gets the first graph out of the list of graphs
        hopcraft(l[0][1])

        end = time.time()
        t = end - start
        print("Execution time: " + str(t))


if __name__ == '__main__':
    unittest.main()
