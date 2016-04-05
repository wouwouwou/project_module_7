import time
import unittest

from colorrefinement import colorrefinement
from graphcomparison.graphcomparison import countautomorphisms, slowcountautomorphisms
from graphs.basicgraphs import graph
from graphs.graphIO import loadgraph, writeDOT


class TestColorRefinement(unittest.TestCase):
    def testIsomorphismCount(self):
        """
        Test for counting Isomorphic graphs
        :return:
        """
        start = time.time()

        # Load a Python tuple of length 2, where the first element is a list of Graphs.
        # l = loadgraph('../test_grafen/colorref_smallexample_2_49.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_4_7.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_4_16.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_6_15.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_largeexample_4_1026.grl', readlist=True)
        l = loadgraph('../test_grafen/torus24.grl', readlist=True)
        # Gets the first graph out of the list of graphs
        # writeDOT(colorrefinement.disjointunion(l[0][2], l[0][0]), "output.dot")
        r = colorrefinement.countiso(l[0][0], l[0][3])
        self.assertEqual(r, 96)
        r = colorrefinement.countiso(l[0][1], l[0][2])
        self.assertEqual(r, 0)
        r = colorrefinement.countiso(l[0][1], l[0][2])
        self.assertEqual(r, 96)
        end = time.time()
        t = end - start
        print("Execution time: " + str(t))

    def testColorAssignment(self):
        """
        Test for colorrefinement
        :return:
        """
        start = time.time()
        print(str(start))

        # Load a Python tuple of length 2, where the first element is a list of Graphs.
        # l = loadgraph('../test_grafen/colorref_smallexample_2_49.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_4_7.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_4_16.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_6_15.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_largeexample_4_1026.grl', readlist=True)
        # l = loadgraph('../test_grafen/torus24.grl', readlist=True)
        l = loadgraph('../test_grafen/circle_4_7.grl', readlist=True)
        # Gets the first graph out of the list of graphs
        g = colorrefinement.slowcolorrefinement(l[0][1])
        writeDOT(g, "output.dot")

        end = time.time()
        t = end - start
        print("Execution time: " + str(t))

    def testFullProgramm(self):
        """
        Test for getting a list with isomorphic graphs.
        :return:
        """
        start = time.time()

        # Load a Python tuple of length 2, where the first element is a list of Graphs.
        # l = loadgraph('../test_grafen/colorref_smallexample_2_49.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_4_7.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_4_16.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_6_15.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_largeexample_4_1026.grl', readlist=True)
        # l = loadgraph('../test_grafen/torus24.grl', readlist=True)
        # l = loadgraph('../test_grafen/trees90.grl', readlist=True)
        # l = loadgraph('../test_grafen/products72.grl', readlist=True)
        l = loadgraph('../test_grafen/circle_4_7.grl', readlist=True)
        graphlist = l[0]
        for g in graphlist:
            colorrefinement.slowcolorrefinement(g)
        print(str(slowcountautomorphisms(l[0][1], l[0][1])))

        end = time.time()
        t = end - start
        print("Execution time: " + str(t))

    def testHoppie(self):
        """
        Test for getting a list with isomorphic graphs.
        :return:
        """
        start = time.time()

        # Load a Python tuple of length 2, where the first element is a list of Graphs.
        # l = loadgraph('../test_grafen/colorref_smallexample_2_49.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_4_7.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_4_16.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_6_15.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_largeexample_4_1026.grl', readlist=True)
        # l = loadgraph('../test_grafen/torus24.grl', readlist=True)
        # l = loadgraph('../test_grafen/trees90.grl', readlist=True)
        # l = loadgraph('../test_grafen/products72.grl', readlist=True)
        graphlist = l[0]
        g = l[0][0]
        g = colorrefinement.colorrefinement(g)
        print(g.getcoloring())
        a = 0

        # choose a vertex in the chosen coloring class and in V(g)
        x = None

        for v in g.getcoloring()[a]:
            x = v
            break

        if x is None:
            raise Exception("failed to choose a vertex in the chosen color class")

        s = copygraph(g)
        colorings = s.getcoloring().copy()
        for v in s.V():
            if x.getlabel() == v.getlabel():
                x = v
                break
        """"""
        colorings[a].remove(x)
        nextclass = max(colorings.keys()) + 1
        setx = set()
        setx.add(x)
        colorings[nextclass] = setx
        s.setcoloring(colorings)
        """"""

        s = colorrefinement.colorrefinement(s)
        print(s.getcoloring())
        s = colorrefinement.colorrefinement(s)
        print(s.getcoloring())

        end = time.time()
        t = end - start
        print("Execution time: " + str(t))

if __name__ == '__main__':
    unittest.main()


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