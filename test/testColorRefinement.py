import unittest
from graphs import basicgraphs
from graphs.graphIO import loadgraph, writeDOT, savegraph
from colorrefinement import colorrefinement
import time


class TestColorRefinement(unittest.TestCase):
    def testIsomorphismCount(self):
        start = time.time()

        # Load a Python tuple of length 2, where the first element is a list of Graphs.
        # l = loadgraph('../test_grafen/colorref_smallexample_2_49.grl', readlist=True)
        l = loadgraph('../test_grafen/colorref_smallexample_4_7.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_4_16.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_6_15.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_largeexample_4_1026.grl', readlist=True)
        # Gets the first graph out of the list of graphs
        writeDOT(colorrefinement.disjointunion(l[0][2], l[0][0]), "output.dot")
        r = colorrefinement.countiso(l[0][1], l[0][3])
        self.assertEqual(r, 1)
        r = colorrefinement.countiso(l[0][1], l[0][2])
        self.assertEqual(r, 0)
        r = colorrefinement.countiso(l[0][0], l[0][2])
        self.assertEqual(r, 8)
        end = time.time()
        t = end - start
        print("Execution time: " + str(t))

    def testColorAssignment(self):
        start = time.time()
        print(str(start))

        # Load a Python tuple of length 2, where the first element is a list of Graphs.
        l = loadgraph('../test_grafen/colorref_smallexample_2_49.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_4_7.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_4_16.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_6_15.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_largeexample_4_1026.grl', readlist=True)
        # Gets the first graph out of the list of graphs
        g = colorrefinement.colorrefinement(l[0][1])
        writeDOT(g, "output.dot")

        end = time.time()
        t = end - start
        print("Execution time: " + str(t))

    def testIsomorphicGraphs(self):
        start = time.time()

        # Load a Python tuple of length 2, where the first element is a list of Graphs.
        # l = loadgraph('../test_grafen/colorref_smallexample_2_49.grl', readlist=True)
        l = loadgraph('../test_grafen/colorref_smallexample_4_7.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_4_16.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_6_15.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_largeexample_4_1026.grl', readlist=True)
        graphlist = l[0]
        i = 0
        for g in graphlist:
            colorrefinement.colorrefinement(g)
        print(colorrefinement.isomorphicgraphs(graphlist))

        end = time.time()
        t = end - start
        print("Execution time: " + str(t))

if __name__ == '__main__':
    unittest.main()
