import time
import unittest

from colorrefinement import colorrefinement
from graphcomparison.graphcomparison import processgraphlist
from graphs.basicgraphs import graph
from graphs.graphIO import loadgraph, writeDOT


class TestColorRefinement(unittest.TestCase):

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
        l = loadgraph('../test_grafen/colorref_smallexample_6_15.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_largeexample_4_1026.grl', readlist=True)
        # l = loadgraph('../test_grafen/torus24.grl', readlist=True)
        # l = loadgraph('../test_grafen/circle_4_7.grl', readlist=True)
        # Gets the first graph out of the list of graphs
        g = colorrefinement.colorrefinement(l[0][1])
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
        # l = loadgraph('../test_grafen/colorref_largeexample_6_960.grl', readlist=True)
        l = loadgraph('../test_grafen/torus24.grl', readlist=True)
        # l = loadgraph('../test_grafen/trees90.grl', readlist=True)
        # l = loadgraph('../test_grafen/products72.grl', readlist=True)
        # l = loadgraph('../test_grafen/circle_4_7.grl', readlist=True)
        # l = loadgraph('../test_grafen/cubes3.grl', readlist=True)
        # l = loadgraph('../test_grafen/cubes4.grl', readlist=True)
        # l = loadgraph('../test_grafen/cubes5.grl', readlist=True)
        # l = loadgraph('../test_grafen/torus144.grl', readlist=True)
        # l = loadgraph('../test_grafen/trees36.grl', readlist=True)
        # l = loadgraph('../test_grafen/torus72.grl', readlist=True)
        # l = loadgraph('../test_grafen/bigtrees1.grl', readlist=True)
        graphlist = l[0]
        processgraphlist(graphlist)

        end = time.time()
        t = end - start
        print("Execution time: " + str(t))

if __name__ == '__main__':
    unittest.main()
