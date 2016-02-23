import unittest
from graphs import basicgraphs
from graphs.graphIO import loadgraph, writeDOT
from colorrefinement import colorrefinement
import time


class TestColorRefinement(unittest.TestCase):
    def testColorAssignment(self):
        start = time.time()
        # Load a Python list of length 2, where the first element is a list of Graphs.
        l = loadgraph('../test_grafen/colorref_smallexample_4_7.grl', readlist=True)
        g = colorrefinement.colorrefinement(l[0][0])
        writeDOT(g, "output.dot")
        end = time.time()
        t = end - start
        print("Execution time: " + str(t))

if __name__ == '__main__':
    unittest.main()
