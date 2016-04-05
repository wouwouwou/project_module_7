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


def hopcraft(g: graph, smallestpartition = False):
    """
     Generate a Minimum DFA as described by the Hopcroft's algorithm
     This algorithm has a worst-case complexity of O(ns log n), with n the number of states and s the different amount of degrees.
     @see https://en.wikipedia.org/wiki/DFA_minimization#Hopcroft.27s_algorithm
     @see https://riunet.upv.es/bitstream/handle/10251/27623/partial%20rev%20determ.pdf?sequence=1 Algorithm 6.1
     :param smallestpartition: Select the smallest partition to refine first.
     :param g: The graph
    """
    # Generate a list of neighbours that have incoming (and possibly outgoing) vertices.
    neighbours = neighbourlist(g, g.isdirected())

    # degrees := {1: p1, 2: p2, ..., n: pn} met px = {v1, v2, ..., vk}
    degrees = dict()

    partition = []

    # Set initial coloring if coloring is not set.
    if not g.getcoloring():
        for v in g.V():
            degree = len(neighbours[v])
            if degree not in degrees.keys():
                degrees[degree] = set()
            degrees[degree].add(v)
    else:
        degrees = g.getcoloring()

    # p := {p1, p2, ..., pn}
    for k in degrees:
        partition.append(degrees[k])

    queue = set(range(len(partition)))
    for pn in range(len(partition)):
        if pn != len(partition) - 1:
            queue.add(pn)

    while queue:
        # Choose and remove a set A from W
        an = queue.pop()
        a = partition[an]

        # Iterate for each degree in degrees
        for color in partition:
            if color != a:
                # Let X be the set of states for which a transition on degree leads to a state in A
                nbs = set()
                for v in a:
                    nbs |= neighbours[v]
                x = nbs & color

                # Iterate for each c in range(len(p)), with x&y and y-x not empty.
                for yN in {c for c in range(len(partition)) if x & partition[c] and partition[c] - x}:
                    # Replace y in p by the two sets x&y and y-x
                    y = partition[yN]
                    partition[yN] = x & y
                    partition.append(y - x)

                    # If y is in w
                    if yN in queue:
                        # Add position of p.add(y - x) to w
                        queue.add(len(partition) - 1)
                    else:
                        # Partition the smallest one.
                        if len(x & y) <= len(y - x):
                            # Add position of x&y in p to w
                            queue.add(yN)
                        else:
                            # Add position of y-x in p to w
                            queue.add(len(partition) - 1)

    coloring = dict()
    for pN in range(len(partition)):
        coloring[pN] = partition[pN]

    return coloring

class TestColorRefinement(unittest.TestCase):
    def testIsomorphismCount(self):
        start = time.time()

        # Load a Python tuple of length 2, where the first element is a list of Graphs.
        # l = loadgraph('../test_grafen/colorref_smallexample_2_49.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_2_49.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_4_16.grl', readlist=True)
        l = loadgraph('../test_grafen/colorref_smallexample_4_7.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_6_15.grl', readlist=True)
        # l = loadgraph('../test_grafen/threepaths10240.gr', readlist=True)
        #   `l = loadgraph('../test_grafen/torus24.grl', readlist=True)
        # l = loadgraph('../test_grafen/trees90.grl', readlist=True)
        # Gets the first graph out of the list of graphs
        graph = hopcraft(l[0][1])

        end = time.time()
        t = end - start
        writeDOT(graph, "output.dot")
        print("Execution time: " + str(t))


if __name__ == '__main__':
    unittest.main()
