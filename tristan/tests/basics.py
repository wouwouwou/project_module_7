# Imports used for testing only
import unittest
import time

from tristan.combinator import combinator
from tristan.isomorphisms import isomorphisms

from graphs.graphIO import loadgraph


class MyTestCase(unittest.TestCase):

    def testAut(self):
        """
        Test for automorphisms between two the same graphs.
        :return:
        """
        start = time.time()
        l = loadgraph('../../test_grafen/basis/basicAut2.gr', readlist=False)
        print(isomorphisms(l, l, True))
        end = time.time()
        t = end - start
        print("Execution time: " + str(t))

    def testGI(self):
        """
        Test for isomorphisms between different graphs.
        :return:
        """
        start = time.time()
        #graphlist = loadgraph('../../test_grafen/basis/basicGI3.grl', readlist=True)
        graphlist = loadgraph('../../test_grafen/cubes5.grl', readlist=True)
        combinator(graphlist, True)
        end = time.time()
        t = end - start
        print("Execution time: " + str(t))

    def testGIAut(self):
        """
        Test for number of automorphisms between different graphs.
        :return:
        """
        start = time.time()
        graphlist = loadgraph('../../test_grafen/basis/basicGIAut.grl', readlist=True)
        combinator(graphlist, True)
        end = time.time()
        t = end - start
        print("Execution time: " + str(t))


if __name__ == '__main__':
    unittest.main()

