import time
import unittest

from colorrefinement import colorrefinement
from graphcomparison.graphcomparison import processgraphlist, isoprocessgraphlist, countautomorphisms
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
        l = loadgraph('../test_grafen/colorref_smallexample_2_49.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_4_7.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_4_16.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_6_15.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_largeexample_4_1026.grl', readlist=True)
        # l = loadgraph('../test_grafen/torus24.grl', readlist=True)
        # l = loadgraph('../test_grafen/circle_4_7.grl', readlist=True)
        # Gets the first graph out of the list of graphs
        g = colorrefinement.slowcolorrefinement(l[0][0])
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
        # l = loadgraph('../test_grafen/bonusGI1.grl', readlist=True)
        # l = loadgraph('../test_grafen/basis/bonusAut1.gr', readlist=False)
        # l = loadgraph('../test_grafen/trees36.grl', readlist=True)
        # l = loadgraph('../test_grafen/torus144.grl', readlist=True)
        l = loadgraph('../test_grafen/torus24.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_4_16.grl', readlist=True)
        # l = loadgraph('../test_grafen/colorref_smallexample_6_15.grl', readlist=True)
        # l = loadgraph('../test_grafen/basis/basicAut1.gr', readlist=True)
        # l = loadgraph('../test_grafen/basis/basicAut2.gr', readlist=True)
        # l = loadgraph('../test_grafen/basis/basicGI1.grl', readlist=True)
        # l = loadgraph('../test_grafen/basis/basicGI2.grl', readlist=True)
        # l = loadgraph('../test_grafen/basis/basicGI3.grl', readlist=True)
        # l = loadgraph('../test_grafen/basis/basicGIAut.grl', readlist=True)
        graphlist = l[0]
        processgraphlist(graphlist)

        end = time.time()
        t = end - start
        print("Execution time: " + str(t))

    def testIsomorphicGraphs(self):
        """
        Test for getting a list with isomorphic graphs.
        :return:
        """
        start = time.time()

        # Load a Python tuple of length 2, where the first element is a list of Graphs.
        # l = loadgraph('../test_grafen/basis/bonusGI1.grl', readlist=True)
        # l = loadgraph('../test_grafen/basis/bonusGI2.grl', readlist=True)
        l = loadgraph('../test_grafen/basis/bonusGI3.grl', readlist=True)
        # l = loadgraph('../test_grafen/basis/basicGI1.grl', readlist=True)
        # l = loadgraph('../test_grafen/basis/basicGI2.grl', readlist=True)
        # l = loadgraph('../test_grafen/basis/basicGI3.grl', readlist=True)
        # l = loadgraph('../test_grafen/basis/basicGIAut.grl', readlist=True)
        graphlist = l[0]
        isoprocessgraphlist(graphlist)

        end = time.time()
        t = end - start
        print("Execution time: " + str(t))

    def testAutomorphismsGraph(self):
        """
        Test for getting a list with isomorphic graphs.
        :return:
        """
        start = time.time()

        # Load a Python tuple of length 2, where the first element is a list of Graphs.
        l = loadgraph('../test_grafen/basis/basicAut1.gr', readlist=False)
        # l = loadgraph('../test_grafen/basis/basicAut2.gr', readlist=True)
        print(countautomorphisms(l, l))

        end = time.time()
        t = end - start
        print("Execution time: " + str(t))

if __name__ == '__main__':
    unittest.main()
