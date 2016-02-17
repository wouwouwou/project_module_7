import unittest
from graphs import basicgraphs
from graphs.graphIO import loadgraph
from colorrefinement import colorrefinement


class TestColorRefinement(unittest.TestCase):
    def testColorRefinement(self):
        # Load a Python list of length 2, where the first element is a list of Graphs.
        L = loadgraph('../test_grafen/colorref_smallexample_4_7.grl', readlist=True)
        colorrefinement.colorrefinement(L[0][0])

if __name__ == '__main__':
    unittest.main()
